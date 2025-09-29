import os
from crewai import Agent, LLM
from dotenv import load_dotenv

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

trader_agent = Agent(
    role="Strategic Stock Trader",
    goal = (
        "Decide whether to Buy, Sell, or Hold a given stock based on live market data, "
        "price movements, and financial analysis with the available data."
    ),
    backstory = (
        "You are a strategic trader with years of experience in timing market entry and exit points. "
        "You rely on real-time stock data, daily price movements, and volume trends to make trading decisions "
        "that optimize returns and reduce risk."
    ),
    llm=llm,
    tools=[],
    verbose=True

)