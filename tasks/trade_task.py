"""
Trading Decision Task with Enhanced Configuration
"""
from crewai import Task
from agents.trader_agent import trader_agent

# Import dependencies first
from tasks.analyse_task import get_stock_analysis
from tasks.fundamental_analysis_task import fundamental_analysis_task

trade_decision = Task(
    description=(
        "Based on comprehensive market data analysis and fundamental analysis insights for {stock_symbol}, "
        "make a strategic trading decision. Your analysis should synthesize:\n\n"

        "1. **Technical Analysis** (from market analyst):\n"
        "   - Current price, daily change, volume trends\n"
        "   - Technical indicators and momentum signals\n"
        "   - Short-term market sentiment\n"
        "   - Support and resistance levels\n\n"

        "2. **Fundamental Analysis** (from fundamental analyst):\n"
        "   - Financial health assessment\n"
        "   - Intrinsic value vs market price\n"
        "   - Long-term growth prospects\n"
        "   - Business quality indicators\n"
        "   - Analyst recommendations (if available)\n\n"

        "3. **Risk-Reward Assessment**:\n"
        "   - Potential upside vs downside\n"
        "   - Risk factors from both technical and fundamental perspectives\n"
        "   - Time horizon considerations\n"
        "   - Market-specific risks\n\n"

        "4. **Position Sizing & Entry Strategy**:\n"
        "   - Recommended position size (conservative/moderate/aggressive)\n"
        "   - Suggested entry points\n"
        "   - Stop-loss levels\n"
        "   - Exit strategy considerations\n\n"

        "Provide a balanced recommendation that considers both short-term market dynamics "
        "and long-term fundamental value. Recommend **Buy**, **Sell**, or **Hold** with "
        "clear reasoning, confidence level, and actionable guidelines."
    ),
    expected_output=(
        "A comprehensive trading recommendation including:\n"
        "- **Final Recommendation**: BUY/SELL/HOLD with confidence level (High/Medium/Low)\n"
        "- **Price Target**: Expected price range based on combined analysis\n"
        "- **Time Horizon**: Short-term (1-3 months) vs Long-term (6-12 months) outlook\n"
        "- **Key Supporting Factors**: Top 3-5 reasons for the recommendation\n"
        "- **Risk Factors**: Main risks to consider\n"
        "- **Entry/Exit Strategy**: Suggested entry points and stop-loss levels\n"
        "- **Position Size**: Recommended allocation (Conservative/Moderate/Aggressive)\n"
        "- **Technical Alignment**: How technical analysis supports/contradicts the decision\n"
        "- **Fundamental Alignment**: How fundamental analysis supports/contradicts the decision\n"
        "- **Alternative Scenarios**: What would change the recommendation\n"
        "- **Action Items**: Clear next steps for the investor"
    ),
    agent=trader_agent,
    async_execution=False,  # Must wait for technical and fundamental analysis
    context=[get_stock_analysis, fundamental_analysis_task]
)
