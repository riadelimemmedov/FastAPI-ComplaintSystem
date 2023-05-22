# Python modules and functions
from enum import Enum


#!RoleType
class RoleType(Enum):
    approver = "Approver"
    complainer = "Complainer"
    admin = "Admin"


#!State
class State(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
