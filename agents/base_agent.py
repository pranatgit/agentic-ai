"""
Base investment agent.

Define BaseAgent as the abstract base for every investment agent, exposing only the abstract 
analyze (*args, **kwargs) method that each agent implements (the four Stage-1 agents take the 
property record; the Stage-2 ROI agent also takes the four Stage-1 results). See the problem 
description for the contract.
"""
