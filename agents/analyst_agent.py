"""
Technical Analyst Agent with Enhanced Configuration
"""
from crewai import Agent
from config.llm_config import get_analyst_llm
from config.config_loader import config
from tools.stock_research_tool import get_stock_price
import logging

logger = logging.getLogger(__name__)

# Get configuration
agent_config = config.get('agents.analyst', {})
max_iterations = agent_config.get('max_iterations', 15)
allow_delegation = agent_config.get('allow_delegation', False)

logger.info(f"Initializing Analyst Agent with max_iter={max_iterations}, delegation={allow_delegation}")

analyst_agent = Agent(
    role="Financial Market Analyst",
    goal=(
        "Perform in-depth evaluations of publicly traded stocks using real-time data, "
        "identifying trends, performance insights, and key financial signals to support decision-making."
    ),
    backstory=(
        "You are a veteran financial analyst with deep expertise in interpreting stock market data, "
        "technical trends, and fundamentals. You specialize in producing well-structured reports that evaluate "
        "stock performance using live market indicators. You focus on providing clear, actionable insights "
        "based on current price movements, volume analysis, and technical patterns."
    ),
    llm=get_analyst_llm(),
    tools=[get_stock_price],
    allow_delegation=allow_delegation,
    max_iter=max_iterations,
    verbose=True
)
