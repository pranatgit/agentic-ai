"""
Human-in-the-loop analyst sign-off.

Implement approve_analysis(compiled_graph, thread_id) and override_analysis(compiled_graph, 
thread_id): when the graph reaches analyst_review_node it calls interrupt() and the run is suspended 
on the checkpointer. These functions resume the SAME run (by its thread_id) with the analyst's 
decision, using LangGraph's Command(resume=...). See the problem description for the resume payload 
and the return contract.
"""
