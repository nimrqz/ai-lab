from typing import Literal
from pydantic import BaseModel


class TicketTriage(BaseModel):
    category: Literal["billing", "technical", "account", "other"]
    urgency: Literal["low", "medium", "high"]
    reply: str


class Invoice(BaseModel):
    vendor: str
    date: str
    total: float
    currency: str


class Summary(BaseModel):
    bullets: list[str]
    actions: list[str]
