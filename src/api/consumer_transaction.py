import asyncio
from pub_sub.consumerTransaction import consumerTransactionApi


async def Transaction():
    await asyncio.create_task(consumerTransactionApi())


asyncio.run(Transaction())
