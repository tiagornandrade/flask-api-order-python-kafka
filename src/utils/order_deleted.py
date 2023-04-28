import asyncio
from consumer import Order


async def OrderDeleted():
    await asyncio.create_task(Order.consumerOrderDeleted())

asyncio.run(OrderDeleted())