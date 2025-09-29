from crewai import Crew

from tasks.analyse_task import get_stock_analysis
from tasks.trade_task import trade_decision
from tasks.fundamental_analysis_task import fundamental_analysis_task
from agents.analyst_agent import analyst_agent
from agents.trader_agent import trader_agent
from agents.fundamental_agent import fundamental_analyst_agent

# Set up task dependencies
trade_decision.context = [get_stock_analysis, fundamental_analysis_task]

stock_crew = Crew(
    agents=[analyst_agent, fundamental_analyst_agent, trader_agent],
    tasks=[get_stock_analysis, fundamental_analysis_task, trade_decision],
    verbose=True
)
