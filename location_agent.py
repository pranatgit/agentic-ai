"""
Location agent (Stage 1).

Implement LocationAgent.analyze (property_record): score the neighbourhood with the LLM from 
the address, the school and crime ratings, the walkability and transit scores, the amenities and the 
commute time, and return a single-item list holding the location score, the tier, the insights and 
the investment potential. Every numeric field the model returns must go through the pre-loaded 
as_number() helper. See the problem description for the exact result keys, the score range, the 
rounding, and the enforced-JSON schema.
"""
