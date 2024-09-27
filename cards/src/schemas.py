from pydantic import BaseModel
from datetime import date
from enum import Enum

class CardType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"

class CardStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    EXPIRED = "expired"

class CardBase(BaseModel):
    issuer: str
    card_number: str
    type: CardType
    status: CardStatus
    cardholder_id: int
    expiration_date: date

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    status: CardStatus

class Card(CardBase):
    id: int

    class Config:
        orm_mode = True