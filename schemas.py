from pydantic import BaseModel

class PaymentCreate(BaseModel):
    amount: float

class PaymentResponse(BaseModel):
    payment_id : str
    amount : float
    status : str
    idempotency_key : str