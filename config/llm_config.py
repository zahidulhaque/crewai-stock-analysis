"""
Centralized LLM Configuration Module - OpenAI Compatible Endpoints Only
"""
import os
from crewai import LLM
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


def get_llm(temperature: float = 0.3, model_override: str = None, max_tokens: int = None):
    """
    Get configured LLM instance for OpenAI-compatible endpoints

    Args:
        temperature: LLM temperature (0.0-1.0). Default 0.3 for balanced creativity
        model_override: Optional model name to override default
        max_tokens: Maximum tokens to generate. If None, uses default per agent type

    Returns:
        LLM: Configured CrewAI LLM instance

    Raises:
        ValueError: If required environment variables are not set
    """
    api_key = os.getenv("API_KEY")
    model_id = model_override or os.getenv("MODEL_ID")
    base_url = os.getenv("MODEL_BASE_URL")

    # Provide helpful error messages
    missing_vars = []
    if not api_key:
        missing_vars.append("API_KEY")
    if not model_id:
        missing_vars.append("MODEL_ID")
    if not base_url:
        missing_vars.append("MODEL_BASE_URL")

    if missing_vars:
        error_msg = (
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please set these in your .env file:\n"
            f"  API_KEY=your_api_key\n"
            f"  MODEL_ID=mistralai/Mistral-7B-Instruct-v0.3  (or your model)\n"
            f"  MODEL_BASE_URL=http://localhost:8000/v1  (or your endpoint)\n"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Configuring LLM: {model_id} at {base_url} with temperature={temperature}, max_tokens={max_tokens}")

    try:
        llm_kwargs = {
            "model": f"openai/{model_id}",
            "base_url": base_url,
            "api_key": api_key,
            "temperature": temperature
        }

        # Add max_tokens if specified
        if max_tokens is not None:
            llm_kwargs["max_tokens"] = max_tokens

        llm = LLM(**llm_kwargs)
        logger.info(f"LLM configured successfully")
        return llm
    except Exception as e:
        error_msg = f"Failed to initialize LLM: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg) from e


def get_analyst_llm():
    """Get LLM configured for technical analyst agent"""
    return get_llm(temperature=0.2, max_tokens=1024)  # Concise technical analysis


def get_fundamental_llm():
    """Get LLM configured for fundamental analyst agent"""
    return get_llm(temperature=0.2, max_tokens=1536)  # Detailed financial analysis


def get_trader_llm():
    """Get LLM configured for trader agent"""
    return get_llm(temperature=0.4, max_tokens=1024)  # Focused trading decisions


def get_planner_llm():
    """Get LLM configured for planner agent"""
    return get_llm(temperature=0.3, max_tokens=768)  # Concise strategic plan


def get_manager_llm():
    """Get LLM configured for manager agent (hierarchical process)"""
    return get_llm(temperature=0.5, max_tokens=512)  # Brief coordination
