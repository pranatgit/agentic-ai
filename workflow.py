"""
Compile the investment graph with a durable SQLite checkpointer.

Implement build_investment_workflow(): compile the graph with a durable checkpointer and return it 
as one cached, process-wide instance. The checkpointer is what makes interrupt()/Command(resume) 
work - graph state is persisted at every eve super-step, so the run can pause at the analyst gate and 
resume later against the same thread_id. See the problem description for the contract.
"""
