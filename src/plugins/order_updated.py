import asyncio
from consumer import Order


async def order_updated():
    await asyncio.create_task(Order.consumer_order_updated())

asyncio.run(order_updated())
