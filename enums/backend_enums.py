from enum import Enum

class UserRole(Enum):
    USER="user"
    ADMIN="admin"

class PaymetStatus(Enum):
    FULLY_PAID="fully paid"
    PARTIALLY_PAID="partially paid"
    NOT_PAID="not paid"

class PaymentMode(Enum):
    ONLINE="online"
    OFFLINE="offline"
    PARTIALLY_ONLINE_AND_OFFLINE="partially online and offline"

class EventStatus(Enum):
    COMPLETED="completed"
    PENDING="pending"
    CANCELED="canceled"