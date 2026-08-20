"""
Central configuration for the Real Estate Investment Analyzer (preloaded).

Associates edit only the env file (GEMINI API KEY, GEMINI MODEL). Every other setting - the 
scoring weights, the decision-ladder thresholds, the folder/db paths, and the report's 
fixed presentation constants - lives here.

Two notes on the original brief:
    *   Its config keys never matched what the decision node read (LOCATION SCORE THRESHOLD vs 
        LOCATION THRESHOLD), so configuration was silently ignored. The names here are the ones the 
        decision node actually uses.
    *   It also loaded three thresholds (price fairness, market growth, condition) that no branch 
        ever referenced. Dead parameters are not carried over every value below is consumed.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class SystemConfig:
    """All system settings in one place."""
    
    # From.env the only values an associate configures
    gemini_api_key: str = os.getenv("GEMINI APT KEY", "") or os.getenv("GOOGLE_APT_KEY", "")
    gemini_model: str = os.getenv("GEMINI MODEL", "gemini-3.1-flash-lite")
    
    # Folders SQLite databases
    data_dir: str = str(PROJECT ROOT / "data")
    investment_db_path: str = str(PROJECT ROOT/ "investments.db")
    checkpoint_db_path: str = str(PROJECT ROOT / "checkpoints.db")
    
    # Weights for the deterministic overall score (sum-1.0)
    location_weight: float = 0.25
    price_weight: float = 0.20
    market_weight: float = 0.20
    condition_weight: float = 0.15
    roi_weight: float = 0.20
    
    # Decision-ladder thresholds
    strong_buy_score: float = 8.0               # band 1 overall score
    buy_score: float = 7.0                      # band 2
    consider_score: float = 6.0                 # band 3; below this is a pass
    location_threshold: float = 7.0             # location floor for STRONG BUY (BUY allows one point lower)
    min_roi: float = 8.0                        # annual ROI %, the BUY floor
    strong_roi_multiple: float = 1.5            # STRONG BUY needs min roi * this 
    consider_roi_multiple: float = 0.75         # CONSIDER needs min_roi * this
    strong_cash_flow: float = 500,0             # monthly cash flow floor for STRONG BUY
    max_risk: float = 6.0                       # risk veto on both buy bands (0-10, higher riskier)
    
    # Risk banding (on the ROI agent's independent risk score, NOT 10 overall)
    high_risk: float = 6.0
    moderate_risk: float = 4.0


config = SystemConfig()


# --- Property validation contract (consumed by nodes/validation_node.py) --- 
REQUIRED_FIELDS = ["address", "listing price", "square_footage", "year_built"]

# --- Report presentation constants (consumed by nodes/decision_node.py+ report_node.py) ---
PRIORITY = {
    "STRONG BUY": "HIGH",
    "BUY": "MEDIUM",
    "CONSIDER": "MEDIUM",
    "PASS": "LOW",
}

ACTION_ITEMS = {
    "STRONG BUY": ["Analyst sign-off required, then move to offer"],
    "BUY": ["Analyst sign-off required before making an offer"],
    "CONSIDER": ["Analyst review - proceed only with the noted conditions"],
    "PASS": ["No action file the record"],
}
     

def validate_config() -> bool:
    """Check critical settings. Raises ValueError when something is wrong.""" 
    if not config.gemini_api_key or config.gemini_api_key.lower().startswith("your"): 
        raise ValueError("GEMINI_API_KEY is missing. Paste your key into the .env file.")
    if not config.gemini_model:
        raise ValueError("GEMINI_MODEL is missing. Set it in the env file.")
        return True
    