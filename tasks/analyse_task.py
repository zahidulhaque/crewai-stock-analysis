"""
Technical Analysis Task with Enhanced Configuration
"""
from crewai import Task
from agents.analyst_agent import analyst_agent

get_stock_analysis = Task(
    description=(
        "Analyze the recent performance of the stock: {stock_symbol}. Use the live stock information tool to retrieve "
        "current price, percentage change, trading volume, and other market data. Provide a summary of "
        "how the stock is performing today and highlight any key observations from the data.\n\n"
        "Focus on:\n"
        "- Current price and daily performance\n"
        "- Volume trends and liquidity\n"
        "- 52-week price range context\n"
        "- Short-term momentum indicators\n"
        "- Any unusual market activity"
    ),
    expected_output=(
        "A clear, bullet-pointed summary of:\n"
        "- Current stock price and currency\n"
        "- Daily price change (absolute and percentage)\n"
        "- Volume and average volume comparison\n"
        "- 52-week high/low context\n"
        "- Overall trend assessment (bullish/bearish/neutral)\n"
        "- Key technical observations and any unusual patterns\n"
        "- Market cap and liquidity assessment"
    ),
    agent=analyst_agent,
    async_execution=True  # Can run in parallel with fundamental analysis
)
