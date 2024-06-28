""" app defualt database and model setup """

import asyncio
import logging

from settings.create_data import CreateData

async def create_database():
    """ function to create the default database """

    data_creator = CreateData()
    create_default_database = asyncio.create_task(data_creator.run())
    await create_default_database

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="run.log", filemode="w")
    asyncio.run(create_database())
