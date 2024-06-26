""" module to interact with the databse """

import logging as lg
import config as cfg

from utils.create_data import CreateData

class DatabaseHandler(CreateData):
    """ module to handle interactions with the database """

    async def add_data(self, table_name: cfg.DatabaseTables, data: dict) -> None:
        """ function to add data to database """
        if table_name == cfg.DatabaseTables.REVIEWS.value:
            review_columns = ", ".join(
                [column.value if column.value != cfg.Reviews.ID.value else "" for column in cfg.Reviews]
            )[1:]
            review_values = ", ".join(["'" + value + "'" for value in data.values()])
            add_review = f"""
                INSERT INTO {cfg.DatabaseTables.REVIEWS.value}({review_columns}) VALUES ({review_values})
            """
            print(add_review)
            await self.connection.execute(add_review)

    def remove_data(self, table_name: cfg.DatabaseTables, data: dict) -> None:
        """ function to remove data from database """
        pass

    async def get_all_books(self) -> dict:
        """ function to get all the available books """
        records = await self.connection.fetch(
            query=f"""SELECT * FROM {cfg.DatabaseTables.BOOKS.value};"""
        )
        return [record[cfg.Books.TITLE.value] for record in records]

    def get_book(self, book: str) -> None:
        """ function to get book details from database """
        pass

    async def get_bookid(self, book_tile: str) -> None:
        """ function to get the book id of the given book """
        records = await self.connection.fetch(
            query=f"""
                SELECT * FROM {cfg.DatabaseTables.BOOKS.value}
                WHERE {cfg.Books.TITLE.value} = '{book_tile}'
            """
        )
        return [record[cfg.Books.ID.value] for record in records][0]

    async def get_reviews(self, book_title: str) -> None:
        """ function to get reviews for the book from database """
        records = await self.connection.fetch(
            query=f"""
            SELECT * FROM {cfg.DatabaseTables.REVIEWS.value}
            INNER JOIN {cfg.DatabaseTables.BOOKS.value}
            ON {cfg.DatabaseTables.BOOKS.value}.{cfg.Books.ID.value} = {cfg.DatabaseTables.REVIEWS.value}.{cfg.Reviews.BOOK_ID.value}
            WHERE {cfg.DatabaseTables.BOOKS.value}.{cfg.Books.TITLE.value} = '{book_title}'
            """
        )
        return [record[cfg.Reviews.REVIEW.value] for record in records]
