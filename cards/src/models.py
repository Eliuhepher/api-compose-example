import enum
from sqlalchemy import Column, Integer, String, Enum, Date
from database import Base



class CardType(enum.Enum):
    """Create CardType Enum."""

    credit = "credit"
    debit = "debit"


class CardStatus(enum.Enum):
    """Create CardStatus Enum."""

    active = "active"
    blocked = "blocked"
    expired = "expired"


class Card(Base):
    """Create Card Model."""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    issuer = Column(String, index=True)
    card_number = Column(String, unique=True, nullable=False, index=True)
    type = Column(Enum(CardType), nullable=False, index=True)
    status = Column(Enum(CardStatus), nullable=False, index=True)
    cardholder_id = Column(Integer, index=True)
    expiration_date = Column(Date, index=True)
