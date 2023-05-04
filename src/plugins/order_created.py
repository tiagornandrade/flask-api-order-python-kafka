import asyncio
from consumer import Order


async def order_created():
    await asyncio.create_task(Order.consumer_order_created())

asyncio.run(order_created())
