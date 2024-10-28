from enum import Enum

class PurchaseStatus(Enum):
    IN_CART = -1
    ALL = 0
    WAIT_FOR_CONFIRMATION = 1
    WAIT_FOR_GETTING = 2
    IN_PROGRESS = 3
    DELIVERED = 4
    CANCELLED = 5