from dotenv import load_dotenv
from crew import stock_crew

load_dotenv()

def stock_analyze(stock_symbol: str, market: str = "auto"):
    """
    Run comprehensive stock analysis using CrewAI agents
    
    Args:
        stock_symbol (str): Stock symbol to analyze (e.g., 'AAPL', 'RELIANCE')
        market (str): Market type - "US", "INDIA", or "auto" for detection
    """
    result = stock_crew.kickoff(inputs={
        "stock_symbol": stock_symbol,
        "market": market
    })
    print(result)

if __name__ == "__main__":
    # Test examples for both markets
    print("=== Testing US Stock Analysis ===")
    stock_analyze("AAPL", "US")
    
    print("\n=== Testing Indian Stock Analysis ===")  
    stock_analyze("RELIANCE", "INDIA")
    
    print("\n=== Testing Auto-Detection ===")
    stock_analyze("MSFT")  # Should auto-detect as US
    stock_analyze("TCS")   # Should auto-detect as INDIA
