import asyncio
from pub_sub.consumerOrder import Order


async def OrderDeleted():
    await asyncio.create_task(Order.consumerOrderDeleted())


asyncio.run(OrderDeleted())
