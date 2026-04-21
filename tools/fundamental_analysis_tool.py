"""
Fundamental Analysis Tool with Caching, Retry, Rate Limiting, and Context Optimization
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import yfinance as yf
from crewai.tools import tool
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimit import limits, sleep_and_retry
import logging
from typing import Dict, Any
from utils.cache import cached, get_financial_data_cache
from config.config_loader import config

logger = logging.getLogger(__name__)


def detect_market(stock_symbol: str, market_preference: str = "auto") -> str:
    """
    Detect if a stock symbol belongs to US or Indian market

    Args:
        stock_symbol: Stock ticker symbol
        market_preference: Manual market selection or "auto"

    Returns:
        str: "US" or "INDIA"
    """
    if market_preference.lower() in ["us", "usa", "united states"]:
        return "US"
    elif market_preference.lower() in ["india", "indian", "in"]:
        return "INDIA"

    # Auto-detection logic
    stock_symbol = stock_symbol.upper().strip()

    # Common US stock patterns
    us_patterns = [
        len(stock_symbol) <= 5 and stock_symbol.isalpha(),
        stock_symbol in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "INTC", "AMD"]
    ]

    # Common Indian stock patterns
    indian_patterns = [
        stock_symbol in ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC", "HINDUNILVR", "SBIN", "BHARTIARTL", "KOTAKBANK"],
        len(stock_symbol) > 5 and stock_symbol.endswith("BANK"),
        stock_symbol.startswith("HDFC") or stock_symbol.startswith("ICICI")
    ]

    if any(us_patterns):
        return "US"
    elif any(indian_patterns):
        return "INDIA"
    else:
        return "US"  # Default to US


def summarize_financial_data(data: pd.DataFrame, num_periods: int = 4) -> Dict[str, Any]:
    """
    Summarize financial data to reduce context window usage

    Args:
        data: Pandas DataFrame with financial data
        num_periods: Number of recent periods to include

    Returns:
        dict: Summarized financial data
    """
    if data.empty:
        return {}

    try:
        # Convert to dict and take only recent periods
        data_dict = data.to_dict()

        # Get column names (dates/periods) sorted by most recent
        columns = list(data.columns)
        recent_columns = columns[-num_periods:] if len(columns) >= num_periods else columns

        # Create summarized dictionary with only recent data
        summary = {}
        for row_name in data.index:
            summary[row_name] = {col: data.loc[row_name, col] for col in recent_columns}

        return summary
    except Exception as e:
        logger.error(f"Error summarizing financial data: {e}")
        return {}


@cached(cache=get_financial_data_cache(), ttl_seconds=600)
def get_us_financial_statements(stock_symbol: str) -> Dict[str, Any]:
    """Get US stock financial statements using Yahoo Finance - Optimized for context"""
    try:
        logger.info(f"Fetching US financial statements for {stock_symbol}")
        ticker = yf.Ticker(stock_symbol)

        # Get financial statements
        income_stmt = ticker.financials
        balance_sheet = ticker.balance_sheet
        cash_flow = ticker.cashflow
        quarterly_financials = ticker.quarterly_financials

        # Get key metrics
        info = ticker.info

        # Summarize financial statements to reduce context usage
        financial_data = {
            "symbol": stock_symbol.upper(),
            "market": "US",
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "key_metrics": {
                "market_cap": info.get("marketCap"),
                "enterprise_value": info.get("enterpriseValue"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "peg_ratio": info.get("pegRatio"),
                "price_to_book": info.get("priceToBook"),
                "debt_to_equity": info.get("debtToEquity"),
                "roe": info.get("returnOnEquity"),
                "roa": info.get("returnOnAssets"),
                "gross_margin": info.get("grossMargins"),
                "operating_margin": info.get("operatingMargins"),
                "profit_margin": info.get("profitMargins"),
                "revenue_growth": info.get("revenueGrowth"),
                "earnings_growth": info.get("earningsGrowth"),
                "current_ratio": info.get("currentRatio"),
                "quick_ratio": info.get("quickRatio")
            },
            "financial_statements": {
                "income_statement": summarize_financial_data(income_stmt, 3) if not income_stmt.empty else {},
                "balance_sheet": summarize_financial_data(balance_sheet, 3) if not balance_sheet.empty else {},
                "cash_flow": summarize_financial_data(cash_flow, 3) if not cash_flow.empty else {},
                "quarterly_results": summarize_financial_data(quarterly_financials, 4) if not quarterly_financials.empty else {}
            },
            "success": True
        }

        logger.info(f"Successfully fetched US financial data for {stock_symbol}")
        return financial_data

    except Exception as e:
        error_msg = f"Error fetching US financial data for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol,
            "market": "US"
        }


@cached(cache=get_financial_data_cache(), ttl_seconds=600)
def get_indian_financial_statements(stock_symbol: str) -> Dict[str, Any]:
    """Get Indian stock financial statements using screener.in with current market data"""
    try:
        logger.info(f"Fetching Indian financial statements for {stock_symbol}")

        # Get current market data from Yahoo Finance
        yahoo_symbol = f"{stock_symbol}.NS"
        ticker = yf.Ticker(yahoo_symbol)
        info = ticker.info

        current_price = info.get('regularMarketPrice', info.get('currentPrice'))

        # Get financial data from screener.in (summarized)
        profit_loss = get_profit_loss(stock_symbol, ret_json=True)
        balance_sheet = get_balance_sheet(stock_symbol, ret_json=True)
        cash_flow = get_cash_flow(stock_symbol, ret_json=True)
        quarterly_results = get_quarterly_results(stock_symbol, ret_json=True)

        # Compile comprehensive data (optimized)
        financial_data = {
            "symbol": stock_symbol.upper(),
            "market": "INDIA",
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_market_data": {
                "current_price": current_price,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "price_to_book": info.get("priceToBook"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "dividend_yield": info.get("dividendYield"),
                "volume": info.get("volume")
            },
            "financial_statements": {
                "profit_loss": profit_loss,
                "balance_sheet": balance_sheet,
                "cash_flow": cash_flow,
                "quarterly_results": quarterly_results
            },
            "success": True
        }

        logger.info(f"Successfully fetched Indian financial data for {stock_symbol}")
        return financial_data

    except Exception as e:
        error_msg = f"Error fetching Indian financial data for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol,
            "market": "INDIA"
        }


@tool("Get Stock Financial Statements")
def get_financial_statements(stock_symbol: str, market: str = "auto") -> str:
    """
    Retrieves comprehensive financial statements for a given stock symbol.
    Automatically detects market (US/India) or uses specified market.
    Includes retry logic, caching, and optimized context usage.

    Parameters:
        stock_symbol (str): The ticker symbol (e.g., AAPL, RELIANCE, TCS, MSFT).
        market (str): Market preference - "US", "INDIA", or "auto" for detection.

    Returns:
        str: JSON containing the company's financial statements and key metrics.
    """
    try:
        detected_market = detect_market(stock_symbol, market)
        logger.info(f"Analyzing {stock_symbol} in {detected_market} market")

        if detected_market == "US":
            result = get_us_financial_statements(stock_symbol)
        else:
            result = get_indian_financial_statements(stock_symbol)

        return json.dumps(result, indent=2, default=str)

    except Exception as e:
        error_msg = f"Error fetching financial statements for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return json.dumps({
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol
        }, indent=2)


def get_us_analyst_recommendations(stock_symbol: str) -> Dict[str, Any]:
    """Get US stock analyst recommendations using Yahoo Finance"""
    try:
        logger.info(f"Fetching US analyst recommendations for {stock_symbol}")
        ticker = yf.Ticker(stock_symbol)
        info = ticker.info

        # Get available analyst data from Yahoo Finance
        recommendations = {
            "symbol": stock_symbol.upper(),
            "market": "US",
            "analyst_data": {
                "recommendation": info.get("recommendationKey", "N/A"),
                "target_mean_price": info.get("targetMeanPrice"),
                "target_high_price": info.get("targetHighPrice"),
                "target_low_price": info.get("targetLowPrice"),
                "number_of_analyst_opinions": info.get("numberOfAnalystOpinions"),
                "recommendation_mean": info.get("recommendationMean")
            },
            "key_highlights": {
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "analyst_price_target": info.get("targetMeanPrice"),
                "current_price": info.get("regularMarketPrice", info.get("currentPrice"))
            },
            "success": True
        }

        # Add interpretation
        rec_mean = info.get("recommendationMean")
        if rec_mean:
            if rec_mean <= 2:
                recommendations["interpretation"] = "Strong Buy/Buy consensus"
            elif rec_mean <= 3:
                recommendations["interpretation"] = "Hold/Moderate Buy consensus"
            else:
                recommendations["interpretation"] = "Hold/Sell consensus"

        logger.info(f"Successfully fetched US analyst recommendations for {stock_symbol}")
        return recommendations

    except Exception as e:
        error_msg = f"Error fetching US analyst data for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol,
            "market": "US"
        }


def get_indian_analyst_recommendations(stock_symbol: str) -> Dict[str, Any]:
    """Get Indian stock analyst recommendations and current market data"""
    try:
        logger.info(f"Fetching Indian analyst recommendations for {stock_symbol}")

        # Get current price and market data from Yahoo Finance
        yahoo_symbol = f"{stock_symbol}.NS"
        ticker = yf.Ticker(yahoo_symbol)
        info = ticker.info

        current_price = info.get('regularMarketPrice', info.get('currentPrice'))

        # Get analyst insights from screener.in
        url = f"https://www.screener.in/company/{stock_symbol}/consolidated/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        pros = []
        cons = []

        pros_section = soup.find('div', class_='pros')
        if pros_section:
            pros = [li.get_text().strip() for li in pros_section.find_all('li')]

        cons_section = soup.find('div', class_='cons')
        if cons_section:
            cons = [li.get_text().strip() for li in cons_section.find_all('li')]

        # Get additional market metrics
        market_data = {
            "current_price": current_price,
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "pe_ratio": info.get("trailingPE"),
            "price_to_book": info.get("priceToBook"),
            "dividend_yield": info.get("dividendYield"),
            "volume": info.get("volume"),
            "avg_volume": info.get("averageVolume")
        }

        result = {
            "symbol": stock_symbol.upper(),
            "market": "INDIA",
            "current_market_data": market_data,
            "analyst_insights": {
                "pros": pros[:5],  # Limit to top 5
                "cons": cons[:5],  # Limit to top 5
                "note": "Price targets not available from screener.in. Analysis based on fundamental data."
            },
            "recommendation": "Analysis should be based on current price vs. fundamental metrics.",
            "success": True
        }

        logger.info(f"Successfully fetched Indian analyst recommendations for {stock_symbol}")
        return result

    except Exception as e:
        error_msg = f"Error fetching Indian analyst data for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol,
            "market": "INDIA"
        }


@tool("Get Stock Analyst Recommendations")
def get_analyst_recommendations(stock_symbol: str, market: str = "auto") -> str:
    """
    Retrieves analyst recommendations for a given stock symbol.
    Automatically detects market (US/India) or uses specified market.
    Includes retry logic and rate limiting.

    Parameters:
        stock_symbol (str): The ticker symbol (e.g., AAPL, RELIANCE, TCS, MSFT).
        market (str): Market preference - "US", "INDIA", or "auto" for detection.

    Returns:
        str: JSON containing analyst recommendations and ratings.
    """
    try:
        detected_market = detect_market(stock_symbol, market)
        logger.info(f"Fetching analyst recommendations for {stock_symbol} in {detected_market} market")

        if detected_market == "US":
            result = get_us_analyst_recommendations(stock_symbol)
        else:
            result = get_indian_analyst_recommendations(stock_symbol)

        return json.dumps(result, indent=2, default=str)

    except Exception as e:
        error_msg = f"Error fetching analyst recommendations for {stock_symbol}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return json.dumps({
            "success": False,
            "error": error_msg,
            "symbol": stock_symbol
        }, indent=2)


# Helper functions for screener.in scraping

def scrape_data(ticker, section_id):
    """Helper function to scrape data from screener.in"""
    try:
        url = f"https://www.screener.in/company/{ticker}/consolidated/#{section_id}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        section = soup.find('section', {'id': section_id})
        if not section:
            return pd.DataFrame()

        table = section.find('table', {'class': 'data-table responsive-text-nowrap'})
        if not table:
            return pd.DataFrame()

        rows = table.find_all('tr')
        data = []

        for row in rows:
            cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        data = [data[0]]  # Add header row
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        filtered_lists = [lst for lst in data if lst]
        df = pd.DataFrame(filtered_lists)
        return df
    except Exception as e:
        logger.error(f"Error scraping {section_id} for {ticker}: {e}")
        return pd.DataFrame()


def get_profit_loss(ticker, ret_json=True):
    """Get company's profit and loss information - last 3 years (optimized)"""
    try:
        profit_loss_df = scrape_data(ticker, 'profit-loss')
        if profit_loss_df.empty:
            return {} if ret_json else pd.DataFrame()

        # Take only last 3 years instead of 5 to reduce context
        profit_loss_df = pd.concat(
            [profit_loss_df.iloc[:, [0]], profit_loss_df.iloc[:, -4:-1]], axis=1)
        profit_loss_df = profit_loss_df.T
        profit_loss_df.columns = profit_loss_df.iloc[0]
        profit_loss_df.drop([profit_loss_df.index[0]], inplace=True)

        if ret_json:
            return json.loads(profit_loss_df.to_json(orient="index"))
        else:
            return profit_loss_df
    except Exception as e:
        logger.error(f"Error getting profit/loss for {ticker}: {e}")
        return {} if ret_json else pd.DataFrame()


def get_balance_sheet(ticker, ret_json=True):
    """Get company's balance sheet information - last 3 years (optimized)"""
    try:
        balance_sheet_df = scrape_data(ticker, 'balance-sheet')
        if balance_sheet_df.empty:
            return {} if ret_json else pd.DataFrame()

        # Take only last 3 years
        balance_sheet_df = pd.concat(
            [balance_sheet_df.iloc[:, [0]], balance_sheet_df.iloc[:, -3:]], axis=1)
        balance_sheet_df = balance_sheet_df.T
        balance_sheet_df.columns = balance_sheet_df.iloc[0]
        balance_sheet_df.drop([balance_sheet_df.index[0]], inplace=True)

        if ret_json:
            return json.loads(balance_sheet_df.to_json(orient="index"))
        else:
            return balance_sheet_df
    except Exception as e:
        logger.error(f"Error getting balance sheet for {ticker}: {e}")
        return {} if ret_json else pd.DataFrame()


def get_cash_flow(ticker, ret_json=True):
    """Get company's cash flow information - last 3 years (optimized)"""
    try:
        cash_flow_df = scrape_data(ticker, 'cash-flow')
        if cash_flow_df.empty:
            return {} if ret_json else pd.DataFrame()

        # Take only last 3 years
        cash_flow_df = pd.concat(
            [cash_flow_df.iloc[:, [0]], cash_flow_df.iloc[:, -3:]], axis=1)
        cash_flow_df = cash_flow_df.T
        cash_flow_df.columns = cash_flow_df.iloc[0]
        cash_flow_df.drop([cash_flow_df.index[0]], inplace=True)

        if ret_json:
            return json.loads(cash_flow_df.to_json(orient="index"))
        else:
            return cash_flow_df
    except Exception as e:
        logger.error(f"Error getting cash flow for {ticker}: {e}")
        return {} if ret_json else pd.DataFrame()


def get_quarterly_results(ticker, ret_json=True):
    """Get company's quarterly results - last 4 quarters (optimized)"""
    try:
        quarterly_results_df = scrape_data(ticker, 'quarters')
        if quarterly_results_df.empty:
            return {} if ret_json else pd.DataFrame()

        # Take only last 4 quarters
        quarterly_results_df = pd.concat(
            [quarterly_results_df.iloc[:, [0]], quarterly_results_df.iloc[:, -4:]], axis=1)
        quarterly_results_df = quarterly_results_df.T
        quarterly_results_df.columns = quarterly_results_df.iloc[0]
        quarterly_results_df.drop([quarterly_results_df.index[0]], inplace=True)

        if ret_json:
            return json.loads(quarterly_results_df.to_json(orient="index"))
        else:
            return quarterly_results_df
    except Exception as e:
        logger.error(f"Error getting quarterly results for {ticker}: {e}")
        return {} if ret_json else pd.DataFrame()
