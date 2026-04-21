"""
Planning Agent for Strategic Analysis Coordination
"""
from crewai import Agent
from config.llm_config import get_planner_llm
from config.config_loader import config
import logging

logger = logging.getLogger(__name__)

# Get configuration
agent_config = config.get('agents.planner', {})
temperature = agent_config.get('temperature', 0.3)
max_iterations = agent_config.get('max_iterations', 1)
allow_delegation = agent_config.get('allow_delegation', False)

logger.info(f"Initializing Planner Agent with temp={temperature}, max_iter={max_iterations}")

planner_agent = Agent(
    role="Stock Analysis Planning Strategist",
    goal=(
        "Create comprehensive and efficient analysis strategies for stocks based on market type, "
        "data availability, and company characteristics. Optimize the analysis workflow to ensure "
        "maximum insight generation while minimizing redundant data collection."
    ),
    backstory=(
        "You are a strategic planning expert with deep knowledge of both US and Indian stock markets. "
        "You excel at designing tailored analysis approaches that account for market-specific nuances, "
        "data source limitations, and company characteristics. Your plans help other agents work more "
        "efficiently by providing clear direction on what to analyze, which metrics to prioritize, "
        "and what challenges to anticipate. You understand the differences between analyzing tech stocks "
        "vs traditional businesses, growth companies vs value stocks, and US vs Indian market dynamics. "
        "You create actionable, step-by-step plans that guide the analysis team to comprehensive insights."
    ),
    llm=get_planner_llm(),
    tools=[],
    allow_delegation=allow_delegation,
    max_iter=max_iterations,
    verbose=True
)
