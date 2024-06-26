""" module to create the frontend page """

import config as cfg
import streamlit as st

from helpers.load_data import LoadData
from utils.manage_database import DatabaseHandler

class CreateWebpage():
    """ class to create the webpage for bookstore """

    def __init__(self, data_handler: DatabaseHandler) -> None:
        self.data_loader = LoadData()
        self.data_handler = data_handler

    async def make_bookdiv(self, book: str) -> None:
        """ function to update the maindiv when a book is selected """
        st.title(book.upper())
        all_reviews = await self.data_handler.get_reviews(book)
        st.subheader("Reviews")
        for review in all_reviews:
            st.text_area(label="", value=review, disabled=True)

    async def make_sidebar(self) -> None:
        """ function to create the sidebar of the UI """
        st.sidebar.title("Book Store".upper())
        st.sidebar.divider()
        reset_button = st.sidebar.button("Reset Database", type="primary", use_container_width=True)

        all_books = await self.data_handler.get_all_books()
        st.sidebar.title("\n\n")
        book_selected = st.sidebar.selectbox(
            "Select Your Book", all_books, index=None, placeholder="Your Book"
        )

        if reset_button:
            await self.data_handler.run()
            st.toast("Database set to initial default value")

        if book_selected is None:
            await self.make_maindiv()
        else:
            await self.make_bookdiv(book_selected)

    async def make_maindiv(self) -> None:
        """ function to create the main central div in the UI """
        st.subheader(cfg.DatabaseTables.BOOKS.value.upper())
        database_dataframe = await self.data_loader.get_dataframe(cfg.DatabaseTables.BOOKS.value)
        st.data_editor(database_dataframe, hide_index=True, use_container_width=True)
        st.divider()
        st.subheader(cfg.DatabaseTables.REVIEWS.value.upper())
        database_dataframe = await self.data_loader.get_dataframe(cfg.DatabaseTables.REVIEWS.value)
        st.data_editor(database_dataframe, hide_index=True, use_container_width=True)

    async def show_frontend(self) -> None:
        """ module entrypoint """
        await self.make_sidebar()
