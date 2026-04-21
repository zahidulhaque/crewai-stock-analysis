"""
Strategic Trader Agent with Enhanced Configuration
"""
from crewai import Agent
from config.llm_config import get_trader_llm
from config.config_loader import config
import logging

logger = logging.getLogger(__name__)

# Get configuration
agent_config = config.get('agents.trader', {})
max_iterations = agent_config.get('max_iterations', 2)
allow_delegation = agent_config.get('allow_delegation', False)

logger.info(f"Initializing Trader Agent with max_iter={max_iterations}, delegation={allow_delegation}")

trader_agent = Agent(
    role="Strategic Stock Trader",
    goal=(
        "Decide whether to Buy, Sell, or Hold a given stock based on live market data, "
        "price movements, and financial analysis with the available data. Synthesize insights "
        "from technical and fundamental analysis to make informed trading decisions."
    ),
    backstory=(
        "You are a strategic trader with years of experience in timing market entry and exit points. "
        "You rely on real-time stock data, daily price movements, volume trends, and fundamental analysis "
        "to make trading decisions that optimize returns and reduce risk. You excel at synthesizing "
        "multiple perspectives - combining short-term technical signals with long-term fundamental value "
        "to create balanced trading strategies. When you need additional information or clarification, "
        "you can delegate questions to the technical analyst or fundamental analyst to ensure your "
        "decisions are well-informed."
    ),
    llm=get_trader_llm(),
    tools=[],
    allow_delegation=allow_delegation,
    max_iter=max_iterations,
    verbose=True
)
