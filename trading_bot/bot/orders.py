from typing import Any

from .client import BinanceFuturesClient


class OrderService:
    """Order placement logic separated from CLI."""

    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def create_order(self, order_data: dict[str, str | None]) -> dict[str, Any]:
        return self.client.place_order(
            symbol=order_data["symbol"],
            side=order_data["side"],
            order_type=order_data["order_type"],
            quantity=order_data["quantity"],
            price=order_data.get("price"),
        )
