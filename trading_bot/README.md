# Simplified Trading Bot - Binance Futures Testnet

A small Python CLI application to place `MARKET` and `LIMIT` orders on Binance USDⓈ-M Futures Testnet.

## Features

- Places MARKET and LIMIT orders
- Supports BUY and SELL sides
- CLI input using `argparse`
- Input validation for symbol, side, order type, quantity, and price
- Separate client/API layer and CLI layer
- Logs API requests, responses, and errors to `logs/trading_bot.log`
- Handles validation errors, Binance API errors, network errors, and unexpected exceptions

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
  logs/
  cli.py
  README.md
  requirements.txt
  .env.example
```

## Setup Steps

### 1. Create Binance Futures Testnet credentials

1. Open Binance Futures Testnet.
2. Register/login.
3. Generate API Key and Secret Key.
4. Keep the keys private and do not upload your `.env` file to GitHub.

The application uses this testnet base URL:

```text
https://testnet.binancefuture.com
```

### 2. Clone/download this project

```bash
git clone <your-github-repo-url>
cd trading_bot
```

### 3. Create virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

For macOS/Linux:

```bash
cp .env.example .env
```

Then update `.env`:

```text
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

## How to Run

### MARKET order example

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT order example

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

For a LIMIT order, `--price` is required.

## Expected Output

```text
========== Order Request Summary ==========
Symbol     : BTCUSDT
Side       : BUY
Order Type : MARKET
Quantity   : 0.001
===========================================

========== Order Response Details =========
Order ID    : 123456789
Status      : FILLED
Executed Qty: 0.001
Avg Price   : 104500.10
Symbol      : BTCUSDT
Side        : BUY
Type        : MARKET
===========================================
SUCCESS: Order placed successfully.
```

## Logs

All logs are saved here:

```text
logs/trading_bot.log
```

The log file includes:

- API request method, URL, and parameters
- API response status code and body
- validation errors
- API errors
- network errors
- unexpected errors

Submit this log file after successfully running at least:

1. one MARKET order
2. one LIMIT order

## Assumptions

- This bot is built only for Binance USDⓈ-M Futures Testnet.
- It does not use real funds.
- LIMIT orders use `timeInForce=GTC` by default.
- API credentials are loaded from a `.env` file.
- Only MARKET and LIMIT orders are implemented as required.

## Important Security Note

Do not commit `.env` or real API keys to GitHub.
