import hashlib
import hmac
import os
import time
from typing import Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from .logging_config import setup_logger

load_dotenv()


class BinanceAPIError(Exception):
    """Raised when Binance returns an error response."""


class BinanceFuturesClient:
    """Small Binance USDT-M Futures Testnet REST client."""

    def __init__(self, api_key: str | None = None, api_secret: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = (base_url or os.getenv("BINANCE_BASE_URL") or "https://testnet.binancefuture.com").rstrip("/")
        self.logger = setup_logger(__name__)

        if not self.api_key or not self.api_secret:
            raise BinanceAPIError(
                "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET in .env"
            )

    def _sign(self, params: dict[str, Any]) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None, signed: bool = False) -> dict[str, Any]:
        params = params or {}
        headers = {"X-MBX-APIKEY": self.api_key}

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000
            params["signature"] = self._sign(params)

        url = f"{self.base_url}{path}"
        safe_params = {k: v for k, v in params.items() if k != "signature"}
        self.logger.info("API request | method=%s | url=%s | params=%s", method, url, safe_params)

        try:
            response = requests.request(method, url, params=params, headers=headers, timeout=15)
            self.logger.info("API response | status_code=%s | body=%s", response.status_code, response.text)
            data = response.json()
        except requests.exceptions.RequestException as exc:
            self.logger.exception("Network error while calling Binance API")
            raise BinanceAPIError(f"Network error: {exc}") from exc
        except ValueError as exc:
            self.logger.exception("Invalid JSON response from Binance API")
            raise BinanceAPIError("Invalid JSON response from Binance API") from exc

        if response.status_code >= 400:
            message = data.get("msg", response.text) if isinstance(data, dict) else response.text
            code = data.get("code", response.status_code) if isinstance(data, dict) else response.status_code
            raise BinanceAPIError(f"Binance API error {code}: {message}")

        return data

    def place_order(self, symbol: str, side: str, order_type: str, quantity: str, price: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "newOrderRespType": "RESULT",
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._request("POST", "/fapi/v1/order", params=params, signed=True)
