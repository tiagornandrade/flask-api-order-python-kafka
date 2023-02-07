import asyncio
from pub_sub.consumerTransaction import consumerTransactionCreated


async def Transaction():
    await asyncio.create_task(consumerTransactionCreated())


asyncio.run(Transaction())