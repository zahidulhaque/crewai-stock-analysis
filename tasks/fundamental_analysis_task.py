"""
Fundamental Analysis Task with Enhanced Configuration
"""
from crewai import Task
from agents.fundamental_agent import fundamental_analyst_agent

fundamental_analysis_task = Task(
    description=(
        "Conduct a comprehensive fundamental analysis of the stock {stock_symbol} in the {market} market. "
        "Adapt your analysis approach based on the market type:\n\n"

        "**For US Stocks (Yahoo Finance Data):**\n"
        "- Analyze SEC-based financial statements (10-K, 10-Q formats)\n"
        "- Focus on US GAAP metrics and ratios\n"
        "- Use analyst price targets and recommendations when available\n"
        "- Evaluate against S&P sector benchmarks\n"
        "- Consider US market dynamics (Fed policy, economic indicators)\n\n"

        "**For Indian Stocks (Screener.in + Yahoo Finance Data):**\n"
        "- Analyze Indian Accounting Standards-based statements from Screener.in\n"
        "- Use current market data from Yahoo Finance (.NS symbols)\n"
        "- **IMPORTANT**: Price targets are NOT reliably available from Screener.in\n"
        "- Focus on fundamental valuation using P/E, P/B, and intrinsic value calculations\n"
        "- Consider Indian market factors (RBI policy, regulatory changes)\n"
        "- Compare against Indian sector benchmarks and peer companies\n\n"

        "**Universal Analysis Framework:**\n"
        "1. **Current Market Data Analysis**:\n"
        "   - Current price vs 52-week range analysis\n"
        "   - Trading volume and liquidity assessment\n"
        "   - Market cap and valuation multiples\n\n"

        "2. **Financial Statements Analysis**:\n"
        "   - Revenue trends, profitability, and margins analysis\n"
        "   - Balance sheet strength and asset quality\n"
        "   - Cash flow generation and capital allocation\n"
        "   - Quarterly performance trends\n\n"

        "3. **Financial Ratios Calculation**:\n"
        "   - Profitability ratios (ROE, ROA, Profit Margins)\n"
        "   - Liquidity ratios (Current, Quick, Cash ratios)\n"
        "   - Leverage ratios (Debt-to-Equity, Interest Coverage)\n"
        "   - Efficiency ratios (Asset Turnover, Working Capital)\n"
        "   - Valuation ratios (P/E, P/B, EV/EBITDA)\n\n"

        "4. **Valuation Analysis**:\n"
        "   - For US stocks: Use analyst price targets if available\n"
        "   - For Indian stocks: Calculate intrinsic value using fundamental metrics\n"
        "   - Relative valuation vs peers and historical multiples\n"
        "   - Growth assumptions and sensitivity analysis\n\n"

        "5. **Investment Recommendation**:\n"
        "   - Clear BUY/HOLD/SELL recommendation with confidence level\n"
        "   - Fair value range based on fundamental analysis\n"
        "   - Risk factors specific to the market and company\n"
        "   - Investment thesis tailored to market characteristics\n\n"

        "**Critical Note**: For Indian stocks, calculate fair value based on fundamental analysis, "
        "peer comparison, and market multiples rather than relying on external price targets."
    ),
    agent=fundamental_analyst_agent,
    expected_output=(
        "A comprehensive market-aware fundamental analysis report containing:\n"
        "- **Executive Summary**: Investment recommendation with current market context\n"
        "- **Current Market Data**: Price, volume, and key market metrics\n"
        "- **Market Classification**: Confirmed market type and data sources used\n"
        "- **Financial Health Assessment**: Statements analysis with market-specific insights\n"
        "- **Key Ratios Analysis**: Calculated ratios with market benchmarks\n"
        "- **Valuation Analysis**: \n"
        "  * For US stocks: Analyst targets + fundamental valuation\n"
        "  * For Indian stocks: Intrinsic value calculation based on fundamentals\n"
        "- **Business Quality Evaluation**: Strengths, weaknesses, and competitive position\n"
        "- **Market-Specific Factors**: Regulatory, currency, and local market considerations\n"
        "- **Risk Assessment**: Market-specific and company-specific risks\n"
        "- **Investment Thesis**: Clear reasoning based on fundamental analysis\n"
        "- **Fair Value Estimate**: Market-appropriate valuation methodology with clear assumptions"
    ),
    async_execution=True  # Can run in parallel with technical analysis
)
