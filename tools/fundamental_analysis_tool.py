import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import yfinance as yf
from crewai.tools import tool


def detect_market(stock_symbol: str, market_preference: str = "auto") -> str:
    """
    Detect if a stock symbol belongs to US or Indian market
    """
    if market_preference.lower() in ["us", "usa", "united states"]:
        return "US"
    elif market_preference.lower() in ["india", "indian", "in"]:
        return "INDIA"
    
    # Auto-detection logic
    stock_symbol = stock_symbol.upper().strip()
    
    # Common US stock patterns
    us_patterns = [
        len(stock_symbol) <= 5 and stock_symbol.isalpha(),  # Most US stocks are 1-5 letters
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
        # Default to US for unknown symbols
        return "US"


@tool("Get Stock Financial Statements")
def get_financial_statements(stock_symbol: str, market: str = "auto") -> str:
    """
    Retrieves comprehensive financial statements for a given stock symbol.
    Automatically detects market (US/India) or uses specified market.
    
    Parameters:
        stock_symbol (str): The ticker symbol (e.g., AAPL, RELIANCE, TCS, MSFT).
        market (str): Market preference - "US", "INDIA", or "auto" for detection.

    Returns:
        str: JSON containing the company's financial statements.
    """
    try:
        detected_market = detect_market(stock_symbol, market)
        
        if detected_market == "US":
            return get_us_financial_statements(stock_symbol)
        else:
            return get_indian_financial_statements(stock_symbol)
            
    except Exception as e:
        return f"Error fetching financial statements for {stock_symbol}: {str(e)}"


def get_us_financial_statements(stock_symbol: str) -> str:
    """Get US stock financial statements using Yahoo Finance"""
    try:
        ticker = yf.Ticker(stock_symbol)
        
        # Get financial statements
        income_stmt = ticker.financials
        balance_sheet = ticker.balance_sheet  
        cash_flow = ticker.cashflow
        quarterly_financials = ticker.quarterly_financials
        
        # Get key metrics
        info = ticker.info
        
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
                "earnings_growth": info.get("earningsGrowth")
            },
            "financial_statements": {
                "income_statement": income_stmt.to_dict() if not income_stmt.empty else {},
                "balance_sheet": balance_sheet.to_dict() if not balance_sheet.empty else {},
                "cash_flow": cash_flow.to_dict() if not cash_flow.empty else {},
                "quarterly_results": quarterly_financials.to_dict() if not quarterly_financials.empty else {}
            }
        }
        
        return json.dumps(financial_data, indent=2, default=str)
        
    except Exception as e:
        return f"Error fetching US financial data for {stock_symbol}: {str(e)}"


def get_indian_financial_statements(stock_symbol: str) -> str:
    """Get Indian stock financial statements using screener.in with current market data"""
    try:
        # Get current market data from Yahoo Finance
        yahoo_symbol = f"{stock_symbol}.NS"
        ticker = yf.Ticker(yahoo_symbol)
        info = ticker.info
        
        current_price = info.get('regularMarketPrice', info.get('currentPrice'))
        
        # Get all financial data from screener.in
        profit_loss = get_profit_loss(stock_symbol)
        balance_sheet = get_balance_sheet(stock_symbol)
        cash_flow = get_cash_flow(stock_symbol)
        quarterly_results = get_quarterly_results(stock_symbol)
        
        # Compile comprehensive data
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
            }
        }
        
        return json.dumps(financial_data, indent=2, default=str)
        
    except Exception as e:
        return f"Error fetching Indian financial data for {stock_symbol}: {str(e)}"


@tool("Get Stock Analyst Recommendations")
def get_analyst_recommendations(stock_symbol: str, market: str = "auto") -> str:
    """
    Retrieves analyst recommendations for a given stock symbol.
    Automatically detects market (US/India) or uses specified market.
    
    Parameters:
        stock_symbol (str): The ticker symbol (e.g., AAPL, RELIANCE, TCS, MSFT).
        market (str): Market preference - "US", "INDIA", or "auto" for detection.

    Returns:
        str: JSON containing analyst recommendations and ratings.
    """
    try:
        detected_market = detect_market(stock_symbol, market)
        
        if detected_market == "US":
            return get_us_analyst_recommendations(stock_symbol)
        else:
            return get_indian_analyst_recommendations(stock_symbol)
            
    except Exception as e:
        return f"Error fetching analyst recommendations for {stock_symbol}: {str(e)}"


def get_us_analyst_recommendations(stock_symbol: str) -> str:
    """Get US stock analyst recommendations using Yahoo Finance"""
    try:
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
            }
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
        
        return json.dumps(recommendations, indent=2, default=str)
        
    except Exception as e:
        return f"Error fetching US analyst data for {stock_symbol}: {str(e)}"


def get_indian_analyst_recommendations(stock_symbol: str) -> str:
    """Get Indian stock analyst recommendations and current market data"""
    try:
        # Get current price and market data from Yahoo Finance
        yahoo_symbol = f"{stock_symbol}.NS"
        ticker = yf.Ticker(yahoo_symbol)
        info = ticker.info
        
        current_price = info.get('regularMarketPrice', info.get('currentPrice'))
        
        # Get analyst insights from screener.in
        url = f"https://www.screener.in/company/{stock_symbol}/consolidated/"
        response = requests.get(url)
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
        
        return json.dumps({
            "symbol": stock_symbol.upper(),
            "market": "INDIA", 
            "current_market_data": market_data,
            "analyst_insights": {
                "pros": pros,
                "cons": cons,
                "note": "Price targets not available from screener.in. Analysis based on fundamental data and current market metrics."
            },
            "recommendation": "Analysis should be based on current price vs. fundamental metrics rather than unavailable price targets."
        }, indent=2, default=str)
        
    except Exception as e:
        return f"Error fetching Indian analyst data for {stock_symbol}: {str(e)}"


def scrape_data(ticker, section_id):
    """Helper function to scrape data from screener.in"""
    url = f"https://www.screener.in/company/{ticker}/consolidated/#{section_id}"
    response = requests.get(url)
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


def get_profit_loss(ticker, ret_json=True):
    """Get company's profit and loss information of last 5 years"""
    try:
        profit_loss_df = scrape_data(ticker, 'profit-loss')
        if profit_loss_df.empty:
            return {} if ret_json else pd.DataFrame()
            
        profit_loss_df = pd.concat(
            [profit_loss_df.iloc[:, [0]], profit_loss_df.iloc[:, -6:-1]], axis=1)
        profit_loss_df = profit_loss_df.T
        profit_loss_df.columns = profit_loss_df.iloc[0]
        profit_loss_df.drop([profit_loss_df.index[0]], inplace=True)
        
        if ret_json:
            return json.loads(profit_loss_df.to_json(orient="index"))
        else:
            return profit_loss_df
    except Exception as e:
        return {} if ret_json else pd.DataFrame()


def get_balance_sheet(ticker, ret_json=True):
    """Get company's balance sheet information of last 5 years"""
    try:
        balance_sheet_df = scrape_data(ticker, 'balance-sheet')
        if balance_sheet_df.empty:
            return {} if ret_json else pd.DataFrame()
            
        balance_sheet_df = pd.concat(
            [balance_sheet_df.iloc[:, [0]], balance_sheet_df.iloc[:, -5:]], axis=1)
        balance_sheet_df = balance_sheet_df.T
        balance_sheet_df.columns = balance_sheet_df.iloc[0]
        balance_sheet_df.drop([balance_sheet_df.index[0]], inplace=True)
        
        if ret_json:
            return json.loads(balance_sheet_df.to_json(orient="index"))
        else:
            return balance_sheet_df
    except Exception as e:
        return {} if ret_json else pd.DataFrame()


def get_cash_flow(ticker, ret_json=True):
    """Get company's cash flow information of last 5 years"""
    try:
        cash_flow_df = scrape_data(ticker, 'cash-flow')
        if cash_flow_df.empty:
            return {} if ret_json else pd.DataFrame()
            
        cash_flow_df = pd.concat(
            [cash_flow_df.iloc[:, [0]], cash_flow_df.iloc[:, -5:]], axis=1)
        cash_flow_df = cash_flow_df.T
        cash_flow_df.columns = cash_flow_df.iloc[0]
        cash_flow_df.drop([cash_flow_df.index[0]], inplace=True)
        
        if ret_json:
            return json.loads(cash_flow_df.to_json(orient="index"))
        else:
            return cash_flow_df
    except Exception as e:
        return {} if ret_json else pd.DataFrame()


def get_quarterly_results(ticker, ret_json=True):
    """Get company's quarterly results information of last 5 quarters"""
    try:
        quarterly_results_df = scrape_data(ticker, 'quarters')
        if quarterly_results_df.empty:
            return {} if ret_json else pd.DataFrame()
            
        quarterly_results_df = pd.concat(
            [quarterly_results_df.iloc[:, [0]], quarterly_results_df.iloc[:, -5:]], axis=1)
        quarterly_results_df = quarterly_results_df.T
        quarterly_results_df.columns = quarterly_results_df.iloc[0]
        quarterly_results_df.drop([quarterly_results_df.index[0]], inplace=True)
        
        if ret_json:
            return json.loads(quarterly_results_df.to_json(orient="index"))
        else:
            return quarterly_results_df
    except Exception as e:
        return {} if ret_json else pd.DataFrame()
