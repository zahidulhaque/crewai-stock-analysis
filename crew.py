"""
Enhanced Stock Analysis Crew with Memory, Planning, and Hierarchical Coordination
"""
from crewai import Crew, Process
from config.config_loader import config
from config.llm_config import get_manager_llm
import logging

# Import agents
from agents.planner_agent import planner_agent
from agents.analyst_agent import analyst_agent
from agents.fundamental_agent import fundamental_analyst_agent
from agents.trader_agent import trader_agent

# Import tasks
from tasks.planning_task import planning_task
from tasks.analyse_task import get_stock_analysis
from tasks.fundamental_analysis_task import fundamental_analysis_task
from tasks.trade_task import trade_decision

logger = logging.getLogger(__name__)

# Get configuration
analysis_config = config.get('analysis', {})
crew_config = config.get('crew', {})
memory_config = crew_config.get('memory_config', {})

enable_memory = analysis_config.get('enable_memory', True)
enable_planning = analysis_config.get('enable_planning', True)
verbose = analysis_config.get('verbose', True)

# Determine process type
process_type = crew_config.get('process', 'sequential')
use_hierarchical = (process_type == 'hierarchical')

logger.info(f"Initializing Stock Analysis Crew: memory={enable_memory}, planning={enable_planning}, process={process_type}")

# Build agent and task lists based on configuration
agents_list = []
tasks_list = []

# Add planning if enabled
if enable_planning:
    agents_list.append(planner_agent)
    tasks_list.append(planning_task)
    logger.info("Planning agent and task added")

# Core agents and tasks
agents_list.extend([analyst_agent, fundamental_analyst_agent, trader_agent])
tasks_list.extend([get_stock_analysis, fundamental_analysis_task, trade_decision])

# Build crew configuration
crew_kwargs = {
    'agents': agents_list,
    'tasks': tasks_list,
    'verbose': verbose,
    'process': Process.hierarchical if use_hierarchical else Process.sequential,
}

# Add memory if enabled
if enable_memory and memory_config.get('enabled', True):
    crew_kwargs['memory'] = True
    logger.info("Memory enabled for crew")

# Add manager LLM for hierarchical process
if use_hierarchical:
    crew_kwargs['manager_llm'] = get_manager_llm()
    logger.info("Hierarchical process enabled with manager LLM")

# Create the crew
stock_crew = Crew(**crew_kwargs)

logger.info(f"Stock Analysis Crew initialized with {len(agents_list)} agents and {len(tasks_list)} tasks")
