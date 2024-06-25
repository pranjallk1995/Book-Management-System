""" app entrypoint """

import asyncio
import logging

import streamlit as st

from utils.create_data import CreateData

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="run.log", filemode="w")
    data_creator = CreateData()
    asyncio.run(data_creator.create_tables())
