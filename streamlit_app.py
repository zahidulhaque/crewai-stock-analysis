import streamlit as st
from dotenv import load_dotenv
import sys
import io
import json
import re

from crew import stock_crew

load_dotenv()

def icon(emoji: str):
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class StreamToExpander(io.StringIO):
    def __init__(self, st_container):
        super().__init__()
        self.st_container = st_container
        self.contents = ""
    def write(self, s):
        self.contents += s
        clean_contents = strip_ansi_codes(self.contents)
        self.st_container.code(clean_contents, language="text")
        return super().write(s)

class StockCrew:
    def __init__(self, stock, market, output_container):
        self.stock = stock
        self.market = market
        self.output_container = output_container
        
    def run(self):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StreamToExpander(self.output_container)
        try:
            result = stock_crew.kickoff(inputs={
                "stock_symbol": self.stock, 
                "market": self.market
            })
        finally:
            sys.stdout = old_stdout
        return mystdout.getvalue(), result

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .analysis-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-container {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'analysis_params' not in st.session_state:
    st.session_state.analysis_params = None
if 'form_stock' not in st.session_state:
    st.session_state.form_stock = ''
if 'form_market' not in st.session_state:
    st.session_state.form_market = 'US Market'
if 'form_analysis' not in st.session_state:
    st.session_state.form_analysis = 'Complete Analysis'

# Main app header
icon("📈")
st.markdown('<h1 class="main-header">Comprehensive Stock Analysis Platform</h1>', unsafe_allow_html=True)
st.subheader("AI-Powered Technical & Fundamental Analysis", divider="rainbow", anchor=False)

# Information section
with st.expander("ℹ️ About This Analysis Platform", expanded=False):
    st.markdown("""
    This platform provides comprehensive stock analysis for **both US and Indian markets** using AI agents that perform:
    
    **🔍 Technical Analysis:**
    - Real-time stock price and market data (Yahoo Finance)
    - Volume trends and momentum indicators
    - Short-term trading signals
    
    **📊 Fundamental Analysis:**
    - **US Stocks**: Yahoo Finance fundamental data (P&L, Balance Sheet, Cash Flow, Key Ratios)
    - **Indian Stocks**: Screener.in financial statements and analyst insights
    - Business health assessment and financial ratio calculations
    - Market-specific analyst recommendations
    
    **💡 Trading Recommendations:**
    - Synthesis of technical and fundamental insights
    - Risk-reward assessment tailored to market dynamics
    - Clear BUY/SELL/HOLD recommendations with confidence levels
    - Entry/exit strategies
    
    **🌍 Supported Markets:**
    - **🇺🇸 US Market**: AAPL, MSFT, TSLA, GOOGL, AMZN, META, NVDA, etc.
    - **🇮🇳 Indian Market**: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, ITC, etc.
    """)
    
    # Market-specific data sources
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🇺🇸 US Data Sources:**
        - Yahoo Finance (Real-time & Fundamentals)
        - SEC filings integration
        - Comprehensive ratio analysis
        """)
    with col2:
        st.markdown("""
        **🇮🇳 Indian Data Sources:**  
        - Yahoo Finance (Real-time prices)
        - Screener.in (Fundamentals)
        - Indian market analyst insights
        """)

# Sidebar configuration
with st.sidebar:
    st.header("🎯 Stock Analysis Configuration")
    
    # Market selection OUTSIDE the form for immediate updates
    st.subheader("Market Selection")
    market_options = ["US Market", "Indian Market"]
    market_index = market_options.index(st.session_state.form_market) if st.session_state.form_market in market_options else 0
    current_market_selection = st.selectbox(
        "Select Market 🌍",
        market_options,
        index=market_index,
        help="Choose the stock market - US or Indian stocks only.",
        key="market_selector"
    )
    
    # Update session state when market changes
    if current_market_selection != st.session_state.form_market:
        st.session_state.form_market = current_market_selection
        st.session_state.form_stock = ''  # Clear stock when market changes
    
    # Stock input form
    with st.form("stock_form"):
        st.subheader("Stock & Analysis Selection")
        
        # Add helpful instruction
        st.info("💡 **Tip**: Select your target market above, then enter the stock symbol for that specific market.")
        
        # Stock input with market-specific placeholder
        if current_market_selection == "US Market":
            placeholder_text = "e.g., AAPL, MSFT, TSLA"
            help_text = "Enter US stock symbols (e.g., AAPL, MSFT, TSLA, GOOGL, AMZN)"
        else:  # Indian Market
            placeholder_text = "e.g., RELIANCE, TCS, INFY"
            help_text = "Enter Indian stock symbols (e.g., RELIANCE, TCS, INFY, HDFCBANK)"
        
        stock = st.text_input(
            "Stock Symbol 📊", 
            value=st.session_state.form_stock,
            placeholder=placeholder_text,
            help=help_text
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        analysis_options = ["Complete Analysis", "Technical Only", "Fundamental Only"]
        analysis_index = analysis_options.index(st.session_state.form_analysis) if st.session_state.form_analysis in analysis_options else 0
        analysis_type = st.selectbox(
            "Analysis Focus",
            analysis_options,
            index=analysis_index,
            help="Choose the type of analysis to perform"
        )
        
        submitted = st.form_submit_button("🚀 Start Analysis", use_container_width=True)
        
        # Store form data in session state when submitted
        if submitted:
            # Update form state
            st.session_state.form_stock = stock.strip().upper()
            st.session_state.form_market = current_market_selection
            st.session_state.form_analysis = analysis_type
            
            # Validate input
            if not stock.strip():
                st.error("Please enter a stock symbol")
                st.stop()
            
            # Store analysis parameters
            st.session_state.analysis_params = {
                'stock': stock.strip().upper(),
                'market_selection': current_market_selection,
                'analysis_type': analysis_type
            }
    
    st.divider()
    
    # Dynamic stock suggestions based on current market selection
    if current_market_selection == "US Market":
        st.subheader("💡 Popular US Stocks")
        sample_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "INTC", "AMD"]
    else:  # Indian Market
        st.subheader("💡 Popular Indian Stocks")  
        sample_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC", "HINDUNILVR", "SBIN", "BHARTIARTL", "KOTAKBANK"]
    
    cols = st.columns(2)
    for i, symbol in enumerate(sample_stocks):
        if cols[i % 2].button(symbol, use_container_width=True, key=f"sample_{symbol}"):
            # Update form state when sample stock is selected
            st.session_state.form_stock = symbol
            st.session_state.form_market = current_market_selection
            st.session_state.form_analysis = "Complete Analysis"
            
            st.session_state.analysis_params = {
                'stock': symbol,
                'market_selection': current_market_selection,
                'analysis_type': "Complete Analysis"
            }
            st.rerun()

# Main analysis execution
if st.session_state.analysis_params:
    params = st.session_state.analysis_params
    stock = params['stock']
    market_selection = params['market_selection']
    analysis_type = params['analysis_type']
    
    # Validation
    if not stock.strip():
        st.error("Please enter a valid stock symbol")
        st.stop()
    
    # Convert market selection to format expected by tools
    market_param = "US" if market_selection == "US Market" else "INDIA"

    # Analysis header with market indication
    market_emoji = "🇺🇸" if market_param == "US" else "🇮🇳"
    st.markdown("---")
    st.subheader(f"🔄 Analysis in Progress for **{stock}** {market_emoji}", anchor=False, divider="rainbow")
    
    # Show current analysis parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📊 **Symbol**: {stock}")
    with col2:
        st.info(f"📍 **Market**: {market_param}")
    with col3:
        st.info(f"⚙️ **Analysis**: {analysis_type}")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Container for live agent output
    with st.expander("🤖 Real-time Agent Execution Log", expanded=True):
        output_container = st.empty()
    
    # Analysis execution
    with st.spinner("Initializing AI agents..."):
        progress_bar.progress(10)
        status_text.text("🔍 Starting technical analysis...")
        
        stock_crew_runner = StockCrew(stock, market_param, output_container)
        
        progress_bar.progress(30)
        if market_param == "US":
            status_text.text("📊 Gathering US fundamental data from Yahoo Finance...")
        else:
            status_text.text("📊 Gathering Indian fundamental data from Screener.in...")
        
        progress_bar.progress(60)
        status_text.text("💡 Generating trading recommendations...")
        
        printed_output, result = stock_crew_runner.run()
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis completed!")
    
    # Results display
    st.markdown("---")
    market_flag = "🇺🇸" if market_param == "US" else "🇮🇳"
    st.subheader(f"📋 Analysis Report for **{stock}** {market_flag}", anchor=False, divider="rainbow")
    
    # Parse and display results
    raw_content = None
    try:
        if hasattr(result, 'raw'):
            raw_content = str(result.raw) if result.raw else None
        elif isinstance(result, str):
            try:
                parsed = json.loads(result)
                raw_content = parsed.get("raw")
            except:
                raw_content = result
        elif isinstance(result, dict):
            raw_content = result.get("raw")
        else:
            raw_content = str(result)
        
        if raw_content and isinstance(raw_content, str):
            raw_content = raw_content.strip()
            
            # Display the analysis in a styled container
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            st.markdown(raw_content)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif raw_content:
            st.markdown(str(raw_content))
        else:
            st.warning("Analysis result is empty. Please check the execution log above.")
            
    except Exception as e:
        st.error(f"Error processing analysis result: {e}")
        st.info("Please check the execution log for details.")
    
    # Download option
    if raw_content:
        st.download_button(
            label="📄 Download Analysis Report",
            data=raw_content,
            file_name=f"{stock}_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Reset option
    if st.button("🔄 Analyze Another Stock", use_container_width=True):
        # Clear all session state
        st.session_state.analysis_params = None
        st.session_state.form_stock = ''
        st.session_state.form_market = 'US Market'
        st.session_state.form_analysis = 'Complete Analysis'
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>⚠️ <strong>Disclaimer:</strong> This analysis is for educational purposes only. Always consult with financial advisors before making investment decisions.</p>
    <p>Built with ❤️ using CrewAI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
