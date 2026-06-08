from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(ValueError):
    """Raised when CLI input is invalid."""


def _positive_decimal(value: str, field_name: str) -> str:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{field_name} must be a valid number.")
    if number <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return format(number, "f")


def validate_order_input(symbol: str, side: str, order_type: str, quantity: str, price: str | None) -> dict:
    symbol = symbol.upper().strip()
    side = side.upper().strip()
    order_type = order_type.upper().strip()

    if not symbol.endswith("USDT") or len(symbol) < 6:
        raise ValidationError("Symbol should be a valid USDT-M futures symbol, e.g. BTCUSDT.")
    if side not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")

    quantity = _positive_decimal(quantity, "Quantity")

    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        price = _positive_decimal(price, "Price")
    else:
        price = None

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
    }
