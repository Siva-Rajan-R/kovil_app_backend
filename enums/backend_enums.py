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

class EventStatus(Enum):
    COMPLETED="completed"
    PENDING="pending"
    CANCELED="canceled"