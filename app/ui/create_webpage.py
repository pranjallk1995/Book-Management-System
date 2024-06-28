""" module to create the frontend page """

import config as cfg
import streamlit as st

# from models.llama3 import get_book_summary

from settings.create_data import CreateData
from handlers.load_data import LoadData
from handlers.manage_database import DatabaseHandler

class CreateWebpage():
    """ class to create the webpage for bookstore """

    def __init__(self, data_handler: DatabaseHandler) -> None:
        self.data_loader = LoadData()
        self.data_handler = data_handler
        self.reset = CreateData()

    async def make_remove_bookdiv(self) -> None:
        """ function to update the maindev when remove book is selected """
        with st.form("remove_book"):
            st.subheader("Book Title".upper())
            book_title = st.text_input(
                label="title", label_visibility="hidden", max_chars=200, placeholder="Book Title..."
            )
            submit = st.form_submit_button("Remove", type="primary")
            if submit:
                await self.data_handler.remove_data(cfg.DatabaseTables.BOOKS, book_title)
                st.toast("Book has been deleted. Refresh Page")

    async def make_add_bookdiv(self) -> None:
        """ function to update the maindiv when add book is selected """
        with st.form("add_book"):
            book_data = {}
            st.subheader("Book Title".upper())
            title = st.text_input(
                label="title", label_visibility="hidden", max_chars=200, placeholder="Book Title..."
            )
            st.subheader("Book Author".upper())
            author = st.text_input(
                label="author", label_visibility="hidden", max_chars=200, placeholder="Book Author..."
            )
            st.subheader("Book Genre".upper())
            genre = st.text_input(
                label="genre", label_visibility="hidden", max_chars=200, placeholder="Book Genre..."
            )
            st.subheader("Publish Date".upper())
            date = st.date_input(
                label="date", label_visibility="hidden", format="YYYY/MM/DD"
            )
            st.divider()
            submit = st.form_submit_button("Add", type="primary")
            if submit:
                book_data[cfg.Books.TITLE.value] = title
                book_data[cfg.Books.AUTHOR.value] = author
                book_data[cfg.Books.GENRE.value] = genre
                book_data[cfg.Books.YEAR.value] = date
                book_data[cfg.Books.SUMMARY.value] = "Summary"
                print(book_data)
                await self.data_handler.add_data(cfg.DatabaseTables.BOOKS, book_data)
                st.toast("Your book is added. Refresh Page")

    async def make_show_bookdiv(self, book: str) -> str:
        """ function to update the maindiv when a book is selected """
        st.title(book.upper())
        all_reviews = await self.data_handler.get_all_reviews(book)
        st.subheader("Reviews")
        for user_id, review in all_reviews:
            if str(user_id) == cfg.USER_ID:
                with st.form("user_review"):
                    st.error(review)
                    delete = st.form_submit_button("Delete", type="primary")
                    if delete:
                        await self.data_handler.remove_data(cfg.DatabaseTables.REVIEWS, book)
                        st.toast("Your review was deleted. Refresh Page")
            else:
                st.error(review)

    async def make_reviewdiv(self, book_title: str) -> None:
        """ function to add a review text area """
        st.divider()
        with st.form("review_data"):
            review_data = {}
            rating = st.slider("Your Rating:", 0, 5, 4, key="rating")
            review = st.text_area(
                label=cfg.USER_ID, placeholder="Your review...",
                label_visibility="hidden", max_chars=5000
            )
            submit = st.form_submit_button("Submit", type="primary")
            if submit:
                review_data[cfg.Reviews.BOOK_ID.value] = str(
                    await self.data_handler.get_bookid(book_title)
                )
                review_data[cfg.Reviews.USER_ID.value] = cfg.USER_ID
                review_data[cfg.Reviews.REVIEW.value] = review
                review_data[cfg.Reviews.RATING.value] = rating
                await self.data_handler.add_data(cfg.DatabaseTables.REVIEWS, review_data)
                st.toast("Your review is added. Refresh Page")

    async def make_sidebar(self) -> None:
        """ function to create the sidebar of the UI """
        st.sidebar.title("Book Store".upper())
        st.sidebar.divider()
        reset_button = st.sidebar.button("Reset Database", type="primary", use_container_width=True)

        for _ in range(1, 4):
            st.sidebar.write("\n")
        st.sidebar.subheader("Manage Book")
        add_book = st.sidebar.button("Add Book", use_container_width=True)
        remove_book = st.sidebar.button("Remove Book", use_container_width=True)

        all_books = await self.data_handler.get_all_books()
        st.sidebar.divider()
        st.sidebar.subheader("Select Your Book")
        book_selected = st.sidebar.selectbox(
            "Select your book:", all_books, index=None,
            placeholder="Your Book", label_visibility="hidden"
        )

        # ===========================================================================
        # fill main container from side bar selection
        # ===========================================================================

        if reset_button:
            await self.reset.drop_tables()
            await self.reset.run()
            st.toast("Database set to initial default value. Refresh Page")

        if book_selected is None and not add_book and not remove_book:
            await self.make_maindiv()
        elif add_book:
            await self.make_add_bookdiv()
        elif remove_book:
            await self.make_remove_bookdiv()
        elif book_selected is not None:
            await self.make_show_bookdiv(book_selected)
            user_review = await self.data_handler.get_review(book_selected)
            if user_review is None:
                await self.make_reviewdiv(book_selected)

    async def make_maindiv(self) -> None:
        """ function to create the main central div in the UI """
        st.subheader(cfg.DatabaseTables.BOOKS.value.upper())
        db_dataframe = await self.data_loader.get_dataframe(cfg.DatabaseTables.BOOKS.value)
        st.data_editor(db_dataframe, hide_index=True, use_container_width=True)
        st.divider()
        st.subheader(cfg.DatabaseTables.REVIEWS.value.upper())
        db_dataframe = await self.data_loader.get_dataframe(cfg.DatabaseTables.REVIEWS.value)
        st.data_editor(db_dataframe, hide_index=True, use_container_width=True)

    async def show_frontend(self) -> None:
        """ module entrypoint """
        await self.make_sidebar()
