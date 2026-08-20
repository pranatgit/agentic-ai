"""
ROI agent (Stage 2) and the INDEPENDENT risk assessor.

Implement ROIAgent.analyze (property_record, location, price, market, condition): this agent CONSUMES 
the four Stage-1 results, which is why it runs in its own stage. Ask the LLM, as an investment 
analyst, to work out the returns from the financials downside - and then to give an INDEPENDENT read of the
downside, on a scale where HIGHER MEANS RISKIER. That risk read is the agent's own judgment of 
what could go wrong; it is NOT the inverse of quality and must never be derived from the overall score. 
Every numeric field the model returns must go through the pre-loaded as_number() helper. See the 
problem description for the exact result keys, the score and risk ranges, the rounding, and the 
enforced-JSON schema.
"""
