""" module to create the frontend page """

import asyncio
import streamlit as st

from helpers.load_data import LoadData

class CreateWebpage():
    """ class to create the webpage for bookstore """

    def __init__(self) -> None:
        self.data_loader = LoadData()

    def show_frontend(self) -> None:
        """ module entrypoint """
        st.title("Book Store")
        st.dataframe(asyncio.run(self.data_loader.get_dataframe("books")))
