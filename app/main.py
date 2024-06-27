""" app entrypoint """

import asyncio
import logging

from ui.create_webpage import CreateWebpage
from handlers.manage_database import DatabaseHandler


async def run_app():
    """ function to start the app execution """

    data_handler = DatabaseHandler()
    connection_status = await data_handler.connect_to_database()
    if connection_status is True:
        create_frontend = asyncio.create_task(CreateWebpage(data_handler).show_frontend())
        await create_frontend

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="run.log", filemode="w")
    asyncio.run(run_app())
