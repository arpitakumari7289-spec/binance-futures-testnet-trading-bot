import argparse
import sys

from bot.client import BinanceAPIError, BinanceFuturesClient
from bot.logging_config import setup_logger
from bot.orders import OrderService
from bot.validators import ValidationError, validate_order_input

logger = setup_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simplified Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "market", "limit"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price", help="Limit price, required for LIMIT orders")
    return parser


def print_summary(order_data: dict) -> None:
    print("\n========== Order Request Summary ==========")
    print(f"Symbol     : {order_data['symbol']}")
    print(f"Side       : {order_data['side']}")
    print(f"Order Type : {order_data['order_type']}")
    print(f"Quantity   : {order_data['quantity']}")
    if order_data.get("price"):
        print(f"Price      : {order_data['price']}")
    print("===========================================\n")


def print_response(response: dict) -> None:
    print("========== Order Response Details =========")
    print(f"Order ID    : {response.get('orderId')}")
    print(f"Status      : {response.get('status')}")
    print(f"Executed Qty: {response.get('executedQty')}")
    print(f"Avg Price   : {response.get('avgPrice')}")
    print(f"Symbol      : {response.get('symbol')}")
    print(f"Side        : {response.get('side')}")
    print(f"Type        : {response.get('type')}")
    print("===========================================")
    print("SUCCESS: Order placed successfully.")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        order_data = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )
        print_summary(order_data)

        client = BinanceFuturesClient()
        service = OrderService(client)
        response = service.create_order(order_data)
        print_response(response)
        return 0

    except ValidationError as exc:
        logger.error("Validation failed: %s", exc)
        print(f"FAILURE: Invalid input - {exc}", file=sys.stderr)
        return 1
    except BinanceAPIError as exc:
        logger.error("Binance/API failure: %s", exc)
        print(f"FAILURE: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"FAILURE: Unexpected error - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
