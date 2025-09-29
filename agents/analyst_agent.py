import os
from crewai import Agent, LLM
from dotenv import load_dotenv

from tools.stock_research_tool import get_stock_price
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

analyst_agent = Agent(
    role="Financial Market Analyst",
    goal = ("Perform in-depth evaluations of publicly traded stocks using real-time data, "
           "identifying trends, performance insights, and key financial signals to support decision-making."),
    backstory = ("You are a veteran financial analyst with deep expertise in interpreting stock market data, "
                 "technical trends, and fundamentals. You specialize in producing well-structured reports that evaluate "
                 "stock performance using live market indicators."),
    llm=llm,
    tools=[get_stock_price],
    verbose=True

)
