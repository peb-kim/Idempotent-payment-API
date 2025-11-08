from fastapi import FastAPI, Header, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from typing import Optional

from .database import Base, engine, get_db
from .models import Payment

app = FastAPI(title="Idempotent Payments API")

#creating database tables at startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/payments")
async def create_payment(
    amount: float, 
    idempotency_key: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Missing Idempotency-Key header")

    #checking if this key alredy exists/used
    result = await db.execute(select(Payment).where(Payment.idempotency_key == idempotency_key))
    existing_payment = result.scalar_one_or_none()

    if existing_payment:
        return {"message": "Duplicate request", "data": {
            "payment_id": existing_payment.payment_id,
            "amount": existing_payment.amount,
            "status": existing_payment.status
        }}

    #processing the payment
    payment_id = str(uuid4())
    payment = Payment(
        payment_id = payment_id,
        amount = amount,
        status = "success",
        idempotency_key = idempotency_key
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    return {"message": "Payment processed", "data": {
        "payment_id": payment.payment_id,
        "amount": payment.amount,
        "status": payment.status
    }}

@app.get("/payments")
async def list_payments(db: AsyncSession = Depends(get_db)):
    result= await db.execute(select(Payment))
    payments = result.scalars().all()
    return {"payments": [
        {"payment_id": p.payment_id, "amount": p.amount, "status": p.status}
        for p in payments
    ]}