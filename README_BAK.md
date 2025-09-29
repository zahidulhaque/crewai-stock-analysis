# CrewAI Hybrid Stock Analysis - US & Indian Markets

A comprehensive stock analysis system using CrewAI agents that provides **dual-market support** for both US and Indian stocks. The system combines technical analysis, fundamental analysis, and trading recommendations with manual market selection and region-specific data sources.

## 🌍 **Hybrid Market Support**

### **Manual Market Selection**
- **Simplified Selection**: Clear choice between "US Market" and "Indian Market"
- **Dynamic Interface**: Stock suggestions and placeholders update based on market selection
- **Dual Data Sources**: Yahoo Finance (US) + Screener.in (Indian) for comprehensive coverage

### **Market-Specific Analysis**
- **🇺🇸 US Stocks**: SEC-based financials, US GAAP ratios, comprehensive Yahoo Finance data
- **🇮🇳 Indian Stocks**: Indian Accounting Standards, BSE/NSE-specific metrics, Screener.in fundamentals
- **Adaptive Methodology**: Analysis approach adapts based on market characteristics

## 🚀 Enhanced Features

### Multi-Agent Analysis System
- **Technical Analyst Agent**: Real-time price analysis (Yahoo Finance - both markets)
- **Hybrid Fundamental Analyst Agent**: Market-aware financial analysis
- **Trading Agent**: Comprehensive recommendations combining insights from both markets

### Market-Aware Analysis Capabilities
- **Technical Analysis**: 
  - Live stock prices, daily changes, volume analysis
  - Universal technical indicators for both markets
- **Fundamental Analysis**: 
  - **US**: Yahoo Finance comprehensive data, SEC filing integration, analyst price targets
  - **India**: Screener.in financial statements, Indian market insights, current pricing from Yahoo Finance
  - **Universal**: Business quality assessment, competitive analysis
- **Trading Recommendations**: 
  - Market-specific risk assessment
  - Currency consideration for international investors
  - Regulatory environment awareness

### Enhanced Web Interface
- **Market Selection Dropdown**: Choose between "US Market" or "Indian Market"
- **Dynamic Stock Suggestions**: Popular stocks update based on market selection
- **Market Indicators**: Visual flags (🇺🇸/🇮🇳) throughout the interface
- **Progress Tracking**: Market-specific data source indicators
- **Comprehensive Reports**: Market-aware analysis presentation

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- API keys for Groq or OpenAI/Local LLM endpoint

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd crewai-stock-analysis
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your API keys:
   ```env
   # Option 1: Using Groq (Recommended)
   GROQ_API_KEY=your_groq_api_key_here
   
   # Option 2: Using Local/OpenAI Compatible API
   API_KEY=your_api_key
   MODEL_ID=your_model_id
   MODEL_BASE_URL=your_model_base_url
   ```

## 🎯 Usage

### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Then open your browser to `http://localhost:8501`

### Market Selection Options:
1. **US Market**: US data sources (Yahoo Finance comprehensive)
2. **Indian Market**: Indian data sources (Screener.in + Yahoo Finance pricing)

### Command Line Interface
```bash
# Specific market analysis
python -c "from main import stock_analyze; stock_analyze('AAPL', 'US')"
python -c "from main import stock_analyze; stock_analyze('RELIANCE', 'INDIA')"
```

## 📊 Supported Stocks & Markets

### 🇺🇸 **US Market Support**
**Data Sources**: Yahoo Finance (comprehensive)
**Popular Stocks**: 
- Tech: `AAPL`, `MSFT`, `GOOGL`, `AMZN`, `META`, `NVDA`, `NFLX`
- Other: `TSLA`, `JPM`, `JNJ`, `PG`, `DIS`, `KO`, `INTC`, `AMD`

**Available Data**:
- Real-time pricing and volume
- SEC-based financial statements (10-K, 10-Q)
- Comprehensive fundamental ratios
- Analyst recommendations and price targets
- US market-specific metrics

### 🇮🇳 **Indian Market Support**
**Data Sources**: Yahoo Finance (pricing) + Screener.in (fundamentals)
**Popular Stocks**:
- Large Cap: `RELIANCE`, `TCS`, `INFY`, `HDFCBANK`, `ICICIBANK`
- Others: `ITC`, `HINDUNILVR`, `SBIN`, `BHARTIARTL`, `KOTAKBANK`, `BOSCHLTD`

**Available Data**:
- Real-time BSE/NSE pricing from Yahoo Finance
- Indian Accounting Standards-based financials from Screener.in
- Current market price and basic metrics
- India-specific business insights and peer comparisons

## 🔧 **Recent Improvements & Bug Fixes**

### **Fixed Issues**:
- **✅ Indian Stock Price Accuracy**: Fixed BOSCHLTD and other Indian stocks showing incorrect current prices
- **✅ Form State Management**: Resolved Streamlit form defaulting to placeholder values
- **✅ Market-Based Suggestions**: Dynamic stock suggestions now update based on market selection
- **✅ Auto-Detect Removal**: Simplified interface by removing confusing auto-detect feature

### **Enhanced Indian Stock Analysis**:
- **Accurate Current Pricing**: Now fetches real-time prices from Yahoo Finance for Indian stocks
- **Reliable Data Sources**: Uses Screener.in for fundamentals with Yahoo Finance for pricing
- **Better Error Handling**: Graceful fallbacks when data sources are unavailable
- **Market Context**: Indian stocks analyzed with appropriate market context and currency (INR)

## 🎯 Sample Analysis Output

### Market-Aware Reports Include:
- **Market Classification**: Confirmed data sources and market type
- **Technical Analysis**: Universal price/volume analysis with current pricing
- **Fundamental Analysis**: Market-specific financial deep-dive
- **Comparative Metrics**: Market-appropriate benchmarking
- **Regulatory Context**: Market-specific compliance and risk factors
- **Currency Considerations**: USD for US stocks, INR for Indian stocks
- **Trading Recommendations**: Market-informed BUY/SELL/HOLD guidance

## 🔧 Architecture

### Hybrid System Components:
- **Manual Market Selection**: Clear US/Indian market choice in interface
- **Dual Data Sources**: Yahoo Finance + Screener.in integration
- **Adaptive Agents**: Market-aware analysis methodology
- **Universal Interface**: Seamless experience for both markets

### Enhanced File Structure:
```
├── agents/
│   ├── fundamental_agent.py      # Hybrid market support
│   ├── analyst_agent.py          # Universal technical analysis
│   └── trader_agent.py           # Market-aware recommendations
├── tasks/
│   ├── fundamental_analysis_task.py  # Market-adaptive analysis
│   └── trade_task.py             # Hybrid recommendation synthesis
├── tools/
│   ├── fundamental_analysis_tool.py  # US + Indian data sources
│   └── stock_research_tool.py    # Universal price data
├── streamlit_app.py              # Market selection interface
└── HYBRID_GUIDE.md              # Detailed usage guide
```

## 🌟 **Key Hybrid Features**

### **1. Simplified Market Selection**
- Clear choice between US Market and Indian Market
- No confusing auto-detection that could fail
- Immediate interface updates based on selection

### **2. Dual Data Integration**
- **US Path**: Yahoo Finance → Comprehensive fundamentals + pricing
- **Indian Path**: Yahoo Finance (pricing) + Screener.in (fundamentals)
- **Error Handling**: Graceful fallbacks between data sources

### **3. Market-Adaptive Analysis**
- **US Focus**: SEC compliance, US GAAP, Fed policy impact, analyst price targets
- **Indian Focus**: Indian regulations, rupee considerations, local market insights
- **Universal**: Technical patterns, volume analysis, momentum

### **4. Enhanced User Experience**
- **Visual Indicators**: Market flags (🇺🇸/🇮🇳) throughout interface
- **Context-Aware Help**: Stock suggestions and placeholders update by market
- **Progress Transparency**: Shows which data sources are being used
- **Form State Persistence**: Remembers user selections across interactions

## ⚠️ **Important Considerations**

### **Data Source Limitations**:
- **US Stocks**: Yahoo Finance rate limits apply
- **Indian Stocks**: Screener.in scraping with respectful delays
- **Real-time Data**: Subject to market hours and data provider delays

### **Market Coverage**:
- **US**: Comprehensive coverage for major exchanges (NYSE, NASDAQ)
- **India**: Focus on BSE/NSE listed companies available on screener.in
- **Other Markets**: Not currently supported

### **Currency & Regulatory**:
- **US**: USD pricing, SEC regulatory framework
- **India**: INR pricing, SEBI regulatory framework  
- **Analysis**: Adapts to market-specific accounting standards

### **Known Limitations**:
- **Indian Price Targets**: Not available from Screener.in; analysis focuses on fundamentals
- **After-Hours Trading**: US after-hours data may not be available
- **Currency Conversion**: Analysis presented in local currency (USD/INR)

## �� **Testing Examples**

### **US Stocks**:
```bash
# Test with popular US stocks
AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA
```

### **Indian Stocks**:
```bash
# Test with popular Indian stocks  
RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, BOSCHLTD
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch  
3. Test with both US and Indian stocks
4. Ensure market selection works correctly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ **Disclaimer**

This hybrid stock analysis tool is designed for educational and research purposes only. The analysis provided should not be considered as financial advice for either US or Indian markets. Always consult with qualified financial advisors familiar with your target market before making investment decisions. The developers are not responsible for any financial losses incurred through the use of this tool.

---

**Built with ❤️ using CrewAI, Yahoo Finance, Screener.in, and Python**  
*Supporting Global Investors with Market-Specific Intelligence*

*Last Updated: September 2025 - Bug fixes for Indian stock pricing and UI improvements*
