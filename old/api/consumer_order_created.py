import asyncio
from pub_sub.consumerOrder import Order


async def OrderCreated():
    await asyncio.create_task(Order.consumerOrderCreated())

asyncio.run(OrderCreated())