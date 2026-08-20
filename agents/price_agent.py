"""
price agent (Stage 1).

Implement PriceAgent.analyze (property_record): as an appraiser, ask the LLM to estimate the market 
value from the comparable properties and judge the asking price against it, returning a single-item 
list holding the estimated value, the price-to-value ratio, the verdict, the pricing score and the 
negotiation points. Note the score key is NOT named after the module. Every numeric field the model 
returns must go through the pre-loaded as_number() helper. See the problem description for the exact 
result keys, the score range, the rounding, and the enforced-JSON schema.
"""
