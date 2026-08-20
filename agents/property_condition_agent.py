"""
Property condition agent (Stage 1).

Implement PropertyConditionAgent.analyze (property_record): as an inspector, ask the LLM to assess 
the property from its age, component conditions, recent updates and known issues, and return a 
single-item list holding the condition score, the tier, the repair estimates and the 
recommendations. Every numeric field the model returns must go through the pre-loaded as_number() 
helper. See the problem description for the exact result keys, the score range, the rounding, 
and the enforced-JSON schema.
"""
