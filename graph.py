"""
LangGraph topology for the real estate investment analyzer.

Define STAGE1_NODES, implement route_after_decision(state), and implement build_investment_graph(): 
a two-stage fan-out / fan-in with a HITL analyst gate. Validate fans out to the four Stage-1 
analyses in parallel; the Stage-2 ROI node waits for ALL FOUR; then coordination, the decision, a 
conditional edge to either the report or the analyst review, and the report. Only the no-action call 
finalises itself - every recommendation to commit capital needs an analyst. Register every node 
under its exact required name; most of them do NOT simply drop the _node suffix. See the problem 
description for the node names, the router contract, and the full edge list.
"""
