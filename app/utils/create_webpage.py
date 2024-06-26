""" module to create the frontend page """

import asyncio

import config as cfg
import streamlit as st

from helpers.load_data import LoadData
from utils.create_data import CreateData

class CreateWebpage():
    """ class to create the webpage for bookstore """

    def __init__(self, data_creator: CreateData) -> None:
        self.data_loader = LoadData()
        self.data_creator = data_creator

    def make_sidebar(self) -> None:
        """ function to create the sidebar of the UI """
        st.sidebar.title("Book Store")
        st.sidebar.divider()
        reset_button = st.sidebar.button("Reset Database", type="primary", use_container_width=True)

        if reset_button:
            asyncio.run(self.data_creator.run())
            st.toast("Database set to initial default value")

    def make_maindiv(self) -> None:
        """ function to create the main central div in the UI """
        st.subheader(cfg.DatabaseTables.BOOKS.value)
        st.dataframe(
            asyncio.run(self.data_loader.get_dataframe(cfg.DatabaseTables.BOOKS.value)),
            hide_index=True, use_container_width=True
        )
        st.divider()
        st.subheader(cfg.DatabaseTables.REVIEWS.value)
        st.dataframe(
            asyncio.run(self.data_loader.get_dataframe(cfg.DatabaseTables.REVIEWS.value)),
            hide_index=True, use_container_width=True
        )

    def show_frontend(self) -> None:
        """ module entrypoint """
        self.make_sidebar()
        self.make_maindiv()
