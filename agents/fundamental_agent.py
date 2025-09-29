import os
from crewai import Agent, LLM
from dotenv import load_dotenv

from tools.fundamental_analysis_tool import get_financial_statements, get_analyst_recommendations

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
API_KEY = os.getenv("API_KEY")

if groq_api_key:
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0
    )
elif API_KEY:
    model_kwargs = {
        "model": f"openai/{os.getenv('MODEL_ID')}",
        "base_url": os.getenv("MODEL_BASE_URL"),
        "api_key": API_KEY
    }
    llm = LLM(**model_kwargs)
    print(f"Using Local LLM endpoint")
else:
    raise ValueError("Authentication error: No valid API key found for GROQ or OpenAI.")

fundamental_analyst_agent = Agent(
    role="Hybrid Fundamental Stock Analyst (US & Indian Markets)",
    goal=(
        "Perform comprehensive fundamental analysis of publicly traded stocks from both US and Indian markets. "
        "Evaluate financial statements, calculate key financial ratios, analyze business health, and provide "
        "investment recommendations based on company fundamentals. Adapt analysis methodology based on "
        "market-specific characteristics and data availability from Yahoo Finance (US) and Screener.in (India)."
    ),
    backstory=(
        "You are a seasoned global fundamental analyst with dual expertise in both US and Indian equity markets. "
        "You have deep knowledge of US GAAP and Indian Accounting Standards, understanding the nuances of "
        "financial reporting in both markets. You specialize in evaluating companies using market-appropriate "
        "methodologies - leveraging SEC filings and comprehensive Yahoo Finance data for US stocks, and "
        "detailed Indian financial statements from Screener.in for Indian stocks. You can interpret different "
        "financial statement formats, calculate relevant ratios for each market, and provide culturally-aware "
        "investment recommendations that account for market-specific factors like regulatory environment, "
        "currency considerations, and local business practices."
    ),
    llm=llm,
    tools=[get_financial_statements, get_analyst_recommendations],
    verbose=True
)
