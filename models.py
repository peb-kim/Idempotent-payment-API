from sqlalchemy import Column, String, Float 
from .database import Base

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, default="success")
    idempotency_key = Column(String, unique=True, nullable=False)