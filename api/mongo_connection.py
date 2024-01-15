import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os


CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING')


async def ping_server(uri: str):
    client = AsyncIOMotorClient(uri)

    try:
        await client.admin.command('ping')
        print('Pinged your deployment. You successfully connected to MongoDB!')
        client.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    localconn = 'mongodb://localhost:27017'
    asyncio.run(ping_server(localconn))
