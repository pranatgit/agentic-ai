"""
Cordinator node.

Implement coordinator_node(state): read the five result lists, assemble component_scores, and 
compute the weighted overall_score (clamped and rounded) using the config weights. Then LIFT the ROI 
agent's own risk_score onto the state - it is the agent's independent read and must NEVER be 
recomputed from the overall score. Also build the coordination_summary. See the problem description 
for the component_scores keys, the summary keys, and the config weights.
"""
