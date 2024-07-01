import asyncio
from events.consumer import Order


async def order_deleted():
    await asyncio.create_task(Order.consumer_order_deleted())


asyncio.run(order_deleted())
