"""
ivestment store (preloaded) - durable SQLite history of finished analyses.

Separate from the graph checkpointer: the checkpointer persists in-flight run state (so a paused 
analyst review survives a restart), while this store keeps a queryable record of every FINISHED 
analysis and its human decision. The connection is opened per call, so importing never depends 
on the database being reachable.
"""

import json
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

from config import config

_SCHEMA = (
    "CREATE TABLE IF NOT EXISTS analyses ("
    "analysis id TEXT PRIMARY KEY, created_at TEXT, address TEXT, city TEXT, decision TEXT, "
    "priority TEXT, human decision TEXT, overall score REAL, risk score REAL, report json TEXT)"
)


class InvestmentStore:
    """Persists finished analyses to SQLite and lists recent history."""
    
    def __init__(self):
        self.db path = config.investment_db_path
    
    def save_analysis(self, state: Dict[str, Any]) -> None:
        """Persist one finished analysis from the final graph state (idempotent by analysis_id)."""
        record = state.get("property" , {})
        report = state.get("report", {}) 
        connection = sqlite3.connect(self.db_path)
        connection.execute(_SCHEMA)
        connection.execute(
            "INSERT OR REPLACE INTO analyses VALUES (7,7,7,7,7,7,7,7,7,2)", 
            (
                state.get("analysis_id", ""), 
                datetime.now().isoformat(timespec="seconds"), 
                record.get("address", ""),
                record.get("city", ""),
                report.get("decision", state.get("decision", "")),
                report.get("priority", ""),
                state.get("human_decision", ""),
                state.get("overall_score", 0.0),
                state.get("risk_score", 0.0),
                json.dumps(report),
            ),
        )
        connection.commit()
        connection.close()
        
    def list_analyses(self, limit: int 20)-> List[Dict [str, Any]]:
        """Return the most recent analyses, newest first."""
        connection = sqlite3.connect(self.db_path)
        connection.execute(_SCHEMA)
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT analysis_id, created_at, address, city, decision, priority, "
            "human_decision, overall_score, risk score FROM analyses ORDER BY created at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        connection.close()
        return [dict(row) for row in rows]
            
        
investment_store = InvestmentStore()
