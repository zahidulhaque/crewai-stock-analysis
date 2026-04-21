"""
Planning Task for Analysis Strategy
"""
from crewai import Task
from agents.planner_agent import planner_agent

planning_task = Task(
    description=(
        "Create a comprehensive analysis strategy for {stock_symbol} in the {market} market. "
        "Consider the following aspects:\n\n"

        "1. **Market Context Assessment**:\n"
        "   - Identify market type (US/India) and associated data sources\n"
        "   - Determine company sector and industry characteristics\n"
        "   - Assess typical valuation metrics for this sector\n\n"

        "2. **Data Collection Strategy**:\n"
        "   - List all data sources to be used (Yahoo Finance, Screener.in, etc.)\n"
        "   - Identify key metrics to focus on based on market and sector\n"
        "   - Determine priority order for data gathering\n\n"

        "3. **Analysis Approach**:\n"
        "   - Technical analysis priorities (price trends, volume, momentum)\n"
        "   - Fundamental analysis priorities (financial ratios, growth metrics, valuation)\n"
        "   - Special considerations for this specific stock/market combination\n\n"

        "4. **Expected Challenges**:\n"
        "   - Data availability issues (especially for Indian stocks)\n"
        "   - Market-specific reporting differences\n"
        "   - Sector-specific analysis nuances\n\n"

        "5. **Analysis Workflow**:\n"
        "   - Step-by-step plan for technical analyst\n"
        "   - Step-by-step plan for fundamental analyst\n"
        "   - Integration approach for trading decision\n\n"

        "Provide a clear, actionable strategy that will guide the analysis team."
    ),
    expected_output=(
        "A comprehensive analysis strategy document containing:\n"
        "- **Market Classification**: Confirmed market type and characteristics\n"
        "- **Data Sources Map**: Which sources to use for each type of data\n"
        "- **Key Metrics Focus List**: Top 10-15 metrics to prioritize\n"
        "- **Analysis Steps**: Detailed workflow for each analyst\n"
        "- **Expected Challenges**: Anticipated obstacles and mitigation strategies\n"
        "- **Success Criteria**: What constitutes a thorough analysis\n"
        "- **Estimated Timeline**: Expected time for each analysis phase"
    ),
    agent=planner_agent
)
