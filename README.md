# CrewAI Hybrid Stock Analysis - US & Indian Markets

  

A comprehensive stock analysis system using CrewAI agents that provides **dual-market support** for both US and Indian stocks. The system combines technical analysis, fundamental analysis, and trading recommendations with manual market selection and region-specific data sources.

  

## 🌍 **Hybrid Market Support**

  

### **Manual Market Selection**

-  **Simplified Selection**: Clear choice between "US Market" and "Indian Market"
-  **Dynamic Interface**: Stock suggestions and placeholders update based on market selection
-  **Dual Data Sources**: Yahoo Finance (US) + Screener.in (Indian) for comprehensive coverage

  

### **Market-Specific Analysis**

-  **🇺🇸 US Stocks**: SEC-based financials, US GAAP ratios, comprehensive Yahoo Finance data
-  **🇮🇳 Indian Stocks**: Indian Accounting Standards, BSE/NSE-specific metrics, Screener.in fundamentals
-  **Adaptive Methodology**: Analysis approach adapts based on market characteristics


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

  

# 📊 CrewAI Stock Analysis

  

## 🛠️ Installation

  

### Prerequisites

- Python 3.8+ (if running locally)
- Docker & Docker Compose (if running via container)
- API keys for your OpenAI-compatible LLM endpoint

---

  

## ⚡ Setup Options


You can start the application in **two ways**:

1.  **Using Python (local environment)**

2.  **Using Docker (containerized)**

  

---

### Prerequisites
- Python 3.8+ (if running locally)
- Docker & Docker Compose (if running via container)
- API keys for your OpenAI-compatible LLM endpoint
  

### **Option 1: Local Installation (Python)**

  

1.  **Clone the repository:**

```bash
git clone crewai-stock-analysis
cd crewai-stock-analysis
```

2.  **Create and activate virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3.  **Install dependencies:**

```bash
pip install -r requirements.txt
```

4.  **Configure environment variables:**

```bash
cp .env.example .env
```
Edit `.env` file with your OpenAI-compatible API configuration:

```bash
# Required: Your API key
API_KEY=your_api_key_here

# Required: Model ID (e.g., meta-llama/Llama-3.1-8B-Instruct)
MODEL_ID=meta-llama/Llama-3.1-8B-Instruct

# Required: Base URL for your OpenAI-compatible endpoint
MODEL_BASE_URL=http://localhost:8000/v1
```

**Supported Endpoints:**
- Local vLLM server
- OpenAI API
- Azure OpenAI
- Any OpenAI-compatible API endpoint


### **Option 2: Using Docker**

#### 🐳 Docker Commands

```bash
# Build and run Streamlit app
docker compose up --build -d

# Stop all services
docker compose down
```

## 🎯 Usage

### Web Interface (Recommended)

If running **locally with Python**:
```bash
streamlit run streamlit_app.py
```
Then open your browser to `http://localhost:8501`
