"""
Pydantic Output Models for Structured Data Validation
"""
from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Optional
from datetime import datetime


class TechnicalAnalysis(BaseModel):
    """Technical analysis output structure"""
    stock_symbol: str = Field(..., description="Stock ticker symbol")
    market: Literal["US", "INDIA"] = Field(..., description="Market type")
    current_price: float = Field(..., description="Current stock price")
    currency: str = Field(default="USD", description="Currency of the price")
    daily_change: float = Field(..., description="Absolute daily price change")
    daily_change_percent: float = Field(..., description="Percentage daily price change")
    volume: Optional[int] = Field(None, description="Trading volume")
    trend: Literal["bullish", "bearish", "neutral"] = Field(..., description="Overall trend direction")
    price_52_week_high: Optional[float] = Field(None, description="52-week high price")
    price_52_week_low: Optional[float] = Field(None, description="52-week low price")
    key_observations: List[str] = Field(..., description="Key technical observations")
    support_level: Optional[float] = Field(None, description="Key support level")
    resistance_level: Optional[float] = Field(None, description="Key resistance level")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")


class FinancialRatios(BaseModel):
    """Financial ratios structure"""
    pe_ratio: Optional[float] = Field(None, description="Price-to-Earnings ratio")
    pb_ratio: Optional[float] = Field(None, description="Price-to-Book ratio")
    debt_to_equity: Optional[float] = Field(None, description="Debt-to-Equity ratio")
    roe: Optional[float] = Field(None, description="Return on Equity")
    roa: Optional[float] = Field(None, description="Return on Assets")
    current_ratio: Optional[float] = Field(None, description="Current ratio")
    quick_ratio: Optional[float] = Field(None, description="Quick ratio")
    profit_margin: Optional[float] = Field(None, description="Profit margin percentage")
    operating_margin: Optional[float] = Field(None, description="Operating margin percentage")
    revenue_growth: Optional[float] = Field(None, description="Revenue growth rate")


class FundamentalAnalysis(BaseModel):
    """Fundamental analysis output structure"""
    stock_symbol: str = Field(..., description="Stock ticker symbol")
    market: Literal["US", "INDIA"] = Field(..., description="Market type")
    company_name: str = Field(..., description="Company name")
    sector: str = Field(..., description="Sector/Industry")
    recommendation: Literal["BUY", "HOLD", "SELL"] = Field(..., description="Investment recommendation")
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(..., description="Confidence level in recommendation")
    fair_value: float = Field(..., description="Calculated fair value per share")
    current_price: float = Field(..., description="Current market price")
    upside_potential: float = Field(..., description="Upside potential in percentage")
    financial_ratios: FinancialRatios = Field(..., description="Key financial ratios")
    strengths: List[str] = Field(..., description="Company strengths")
    weaknesses: List[str] = Field(..., description="Company weaknesses")
    risks: List[str] = Field(..., description="Key investment risks")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    investment_thesis: str = Field(..., description="Investment thesis summary")
    data_sources: List[str] = Field(..., description="Data sources used")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")


class TradingDecision(BaseModel):
    """Trading decision output structure"""
    stock_symbol: str = Field(..., description="Stock ticker symbol")
    market: Literal["US", "INDIA"] = Field(..., description="Market type")
    action: Literal["BUY", "SELL", "HOLD"] = Field(..., description="Trading action")
    confidence: Literal["HIGH", "MEDIUM", "LOW"] = Field(..., description="Confidence level")
    price_target: float = Field(..., description="Price target")
    stop_loss: Optional[float] = Field(None, description="Suggested stop-loss level")
    time_horizon: Literal["short-term", "medium-term", "long-term"] = Field(
        ..., description="Investment time horizon"
    )
    position_size: Literal["conservative", "moderate", "aggressive"] = Field(
        ..., description="Recommended position sizing"
    )
    entry_points: List[float] = Field(..., description="Suggested entry price points")
    key_supporting_factors: List[str] = Field(..., description="Top reasons for the decision")
    risk_factors: List[str] = Field(..., description="Main risks to consider")
    technical_alignment: bool = Field(..., description="Technical analysis supports decision")
    fundamental_alignment: bool = Field(..., description="Fundamental analysis supports decision")
    reasoning: str = Field(..., description="Detailed reasoning for the decision")
    alternative_scenarios: Optional[Dict[str, str]] = Field(
        None, description="Alternative scenarios and actions"
    )
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Decision timestamp")


class PlanningStrategy(BaseModel):
    """Planning strategy output structure"""
    stock_symbol: str = Field(..., description="Stock ticker symbol")
    market: Literal["US", "INDIA"] = Field(..., description="Market type")
    analysis_approach: str = Field(..., description="Recommended analysis approach")
    data_sources: List[str] = Field(..., description="Data sources to use")
    key_metrics_to_focus: List[str] = Field(..., description="Key metrics to focus on")
    analysis_steps: List[str] = Field(..., description="Step-by-step analysis plan")
    expected_challenges: List[str] = Field(..., description="Expected challenges")
    special_considerations: List[str] = Field(..., description="Market-specific considerations")
    estimated_time: str = Field(..., description="Estimated analysis time")
