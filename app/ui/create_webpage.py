""" module to create the frontend page """

import config as cfg
import streamlit as st

from settings.create_data import CreateData
from handlers.load_data import LoadData
from handlers.manage_database import DatabaseHandler

class CreateWebpage():
    """ class to create the webpage for bookstore """

    def __init__(self, data_handler: DatabaseHandler) -> None:
        self.data_loader = LoadData()
        self.data_handler = data_handler
        self.reset = CreateData()

    async def make_bookdiv(self, book: str) -> str:
        """ function to update the maindiv when a book is selected """
        st.title(book.upper())
        all_reviews = await self.data_handler.get_reviews(book)
        st.subheader("Reviews")
        for user_id, review in all_reviews:
            if str(user_id) == cfg.USER_ID:
                with st.form("user_review"):
                    st.error(review)
                    delete = st.form_submit_button("Delete Review", type="primary")
                    if delete:
                        await self.data_handler.remove_data(cfg.DatabaseTables.REVIEWS, book)
                        st.toast("Your review was deleted")
            else:
                st.error(review)

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
            await self.reset.drop_tables()
            await self.reset.run()
            st.toast("Database set to initial default value")

        if book_selected is None:
            div_holder = st.empty()
            with div_holder.container():
                await self.make_maindiv()
        else:
            await self.make_bookdiv(book_selected)
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
                        await self.data_handler.get_bookid(book_selected)
                    )
                    review_data[cfg.Reviews.USER_ID.value] = cfg.USER_ID
                    review_data[cfg.Reviews.REVIEW.value] = review
                    review_data[cfg.Reviews.RATING.value] = rating
                    await self.data_handler.add_data(cfg.DatabaseTables.REVIEWS, review_data)
                    st.toast("Your review is added")

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
