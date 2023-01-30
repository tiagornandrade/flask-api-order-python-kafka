import asyncio
from pub_sub.consumerOrder import consumerOrderApi


async def Order():
    await asyncio.create_task(consumerOrderApi())


asyncio.run(Order())
