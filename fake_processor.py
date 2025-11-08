import asyncio
import random

async def process_payment(amount: float):
    await asyncio.sleep(1)

    if random.random() < 0.95:
        return {"status": "success"}
    else:
        return {"status": "failed"}