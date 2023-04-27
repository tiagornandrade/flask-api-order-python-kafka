import asyncio
from consumer import Order


async def OrderCreated():
    await asyncio.create_task(Order.consumerOrderCreated())

asyncio.run(OrderCreated())