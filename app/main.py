""" app entrypoint """

import asyncio
import logging

from utils.create_webpage import CreateWebpage
from utils.manage_database import DatabaseHandler

async def run_app():
    """ function to start the app execution """
    logging.basicConfig(level=logging.INFO, filename="run.log", filemode="w")

    data_handler = DatabaseHandler()
    await data_handler.run()

    await CreateWebpage(data_handler).show_frontend()

if __name__ == "__main__":
    asyncio.run(run_app())
