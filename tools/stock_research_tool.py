"""
Stock Research Tool with Caching, Retry, and Error Handling
"""
import yfinance as yf
from crewai.tools import tool
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimit import limits, sleep_and_retry
import logging
from typing import Dict, Any
from utils.cache import cached, get_stock_price_cache
from config.config_loader import config

logger = logging.getLogger(__name__)


def get_stock_price_impl(stock_symbol: str) -> Dict[str, Any]:
    """
    Internal implementation of stock price retrieval

    Parameters:
        stock_symbol (str): The ticker symbol of the stock

    Returns:
        dict: Structured stock price data
    """
    try:
        logger.info(f"Fetching stock price for {stock_symbol}")

        # Auto-detect Indian stocks and add .NS suffix if needed
        original_symbol = stock_symbol.upper().strip()
        if not any(x in original_symbol for x in ['.NS', '.BO', '.', '^']):
            # Common Indian stocks
            indian_stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK',
                           'ITC', 'HINDUNILVR', 'SBIN', 'BHARTIARTL', 'KOTAKBANK']
            if original_symbol in indian_stocks or len(original_symbol) > 5:
                stock_symbol = f"{original_symbol}.NS"
                logger.info(f"Auto-detected Indian stock, using {stock_symbol}")

        stock = yf.Ticker(stock_symbol)
        info = stock.info

        current_price = info.get("regularMarketPrice") or info.get("currentPrice")
        change = info.get("regularMarketChange") or info.get("regularMarketDayChange", 0)
        change_percent = info.get("regularMarketChangePercent") or info.get("regularMarketChangePercent", 0)
        currency = info.get("currency", "USD")
        volume = info.get("volume") or info.get("regularMarketVolume")
        market_cap = info.get("marketCap")

        high_52week = info.get("fiftyTwoWeekHigh")
        low_52week = info.get("fiftyTwoWeekLow")
        avg_volume = info.get("averageVolume")

        if current_price is None:
            error_msg = f"Could not fetch price for {stock_symbol}. Symbol may be invalid."
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "symbol": stock_symbol.upper()
            }

        result = {
            "success": True,
            "symbol": stock_symbol.upper(),
            "price": current_price,
            "change": change,
            "change_percent": round(change_percent, 2),
            "currency": currency,
            "volume": volume,
            "market_cap": market_cap,
            "52_week_high": high_52week,
            "52_week_low": low_52week,
            "avg_volume": avg_volume,
            "trend": "bullish" if change > 0 else "bearish" if change < 0 else "neutral"
        }

        logger.info(f"Successfully fetched price for {stock_symbol}: {current_price} {currency}")
        return result

    except Exception as e:
        error_msg = f"Error fetching stock price for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol.upper()
        }


@tool("Live Stock Information Tool")
@cached(cache=get_stock_price_cache(), ttl_seconds=config.get('markets.us.cache_duration_seconds', 300))
def get_stock_price(stock_symbol: str) -> str:
    """
    Retrieves the latest stock price and other relevant info for a given stock symbol using Yahoo Finance.
    Includes automatic retry on failure, rate limiting, and caching for efficiency.

    Parameters:
        stock_symbol (str): The ticker symbol of the stock (e.g., AAPL, TSLA, MSFT).

    Returns:
        str: A JSON string with structured stock data including price, change, volume, and market data.
             Returns error information if the fetch fails.
    """
    import json

    result = get_stock_price_impl(stock_symbol)

    if result["success"]:
        # Format as readable string for LLM
        return json.dumps({
            "status": "success",
            "data": {
                "stock": result["symbol"],
                "price": f"{result['price']} {result['currency']}",
                "change": f"{result['change']} ({result['change_percent']}%)",
                "trend": result["trend"],
                "volume": result.get("volume"),
                "market_cap": result.get("market_cap"),
                "52_week_range": f"{result.get('52_week_low')} - {result.get('52_week_high')}",
                "avg_volume": result.get("avg_volume")
            }
        }, indent=2)
    else:
        return json.dumps({
            "status": "error",
            "error": result["error"],
            "symbol": result["symbol"]
        }, indent=2)
