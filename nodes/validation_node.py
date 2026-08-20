"""
Validation node.

Implement validation_node(state): confirm the property record carries every field in the pre-loaded
REQUIRED_FIELDS. Record any missing field in errors rather than raising. An unassessable property 
must never be auto-recommended for purchase, so an incomplete record is filed as a NO-ACTION call.
See the problem description for the errors entry shape, the no-action token, and the return 
contract.
"""
