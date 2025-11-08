# Idempotent Payments API

A FastAPI project demonstrating idempotent payment processing. 

## Features
- POST /payments with `Idempotency-Key` header to prevent duplicate payments
- GET /payments to list all processed payments
- Uses SQLite with SQLAlchemy (async) for persistent storage
- Simple in-memory caching for duplicate request detection

## Usage
Start the server:
    uvicorn main:app --reload
    Open API docs: http://127.0.0.1:8000/docs
    Use POST /payments with amount and Idempotency-Key to create payments
    Use GET /payments to see all payments