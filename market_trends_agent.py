"""
Market trends agent (Stage 1).

Implement Market TrendsAgent.analyze (property_record): ask the LLM to read the local market from the 
price history, the days on market, the inventory and the price reductions, and return a single-item 
list holding the market score, the temperature, the trend direction, the annual appreciation and the 
forecast. Every numeric field the model returns must go through the pre-loaded as_number() helper. 
See the problem description for the exact result keys, the score range, the rounding, and the 
enforced-JSON schema.
"""
