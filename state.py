"""
Shared workflow state (LangGraph).

Define InvestmentState as a TypedDict carrying the analysis identity and the property record, the 
four Stage-1 result keys, the Stage-2 ROI result, the coordination summary, the overall score and 
the risk score, the decision with its priority, risk level and metrics, the analyst's decision, the 
report, the completion flag, and errors. Every node returns a PARTIAL update; each Stage-1 node 
writes its OWN result key (single-writer), and errors uses a reducer so parallel nodes can append 
safely. Note that risk_score is the ROI agent's INDEPENDENT read of the downside - it is not derived 
from the overall score. See the problem description for the exact key names and the reducer.
"""
