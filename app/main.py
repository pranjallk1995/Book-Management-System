""" app entrypoint """

import asyncio
import logging

from utils.create_data import CreateData
from utils.create_webpage import CreateWebpage

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="run.log", filemode="w")

    data_creator = CreateData()
    asyncio.run(data_creator.run())

    CreateWebpage(data_creator).show_frontend()
