import asyncio
from consumer import Order


async def OrderUpdated():
    await asyncio.create_task(Order.consumerOrderUpdated())

asyncio.run(OrderUpdated())