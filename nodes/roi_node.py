"""
ROI analysis node (Stage 2).

Implement roi_node(state): the graph holds this node until ALL FOUR Stage-1 nodes have finished. 
Read the first entry of each of the four Stage-1 result lists and run ROIAgent on the property 
record plus those four. Skip when the record was already filed as a no-action call at validation, 
and record a failure in errors instead of raising. See the problem description for the return 
contract.
"""
