"""
Main Entry Point for Stock Analysis with Enhanced Logging and Configuration
"""
from dotenv import load_dotenv
from crew import stock_crew
from utils.logging_config import setup_logging
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Setup logging (automatically done when importing logging_config)
logger = logging.getLogger(__name__)


def stock_analyze(stock_symbol: str, market: str = "auto"):
    """
    Run comprehensive stock analysis using CrewAI agents

    Args:
        stock_symbol (str): Stock symbol to analyze (e.g., 'AAPL', 'RELIANCE')
        market (str): Market type - "US", "INDIA", or "auto" for detection
    """
    start_time = datetime.now()
    logger.info(f"=" * 80)
    logger.info(f"Starting stock analysis for {stock_symbol} (market: {market})")
    logger.info(f"=" * 80)

    try:
        result = stock_crew.kickoff(inputs={
            "stock_symbol": stock_symbol,
            "market": market
        })

        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Analysis completed successfully in {elapsed_time:.2f} seconds")

        print("\n" + "=" * 80)
        print(f"ANALYSIS RESULTS FOR {stock_symbol}")
        print("=" * 80)
        print(result)
        print("=" * 80 + "\n")

        return result

    except Exception as e:
        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"Analysis failed after {elapsed_time:.2f} seconds: {str(e)}", exc_info=True)
        print(f"\n❌ Error analyzing {stock_symbol}: {str(e)}\n")
        return None


if __name__ == "__main__":
    logger.info("Stock Analysis CLI started")

    # Test examples for both markets
    print("\n" + "=" * 80)
    print("=== Testing US Stock Analysis ===")
    print("=" * 80 + "\n")
    stock_analyze("AAPL", "US")

    print("\n" + "=" * 80)
    print("=== Testing Indian Stock Analysis ===")
    print("=" * 80 + "\n")
    stock_analyze("RELIANCE", "INDIA")

    print("\n" + "=" * 80)
    print("=== Testing Auto-Detection ===")
    print("=" * 80 + "\n")
    stock_analyze("MSFT")  # Should auto-detect as US
    stock_analyze("TCS")   # Should auto-detect as INDIA

    logger.info("Stock Analysis CLI completed")
