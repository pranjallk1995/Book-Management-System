""" module to interact with the databse """

import config as cfg
import asyncpg as apg
import streamlit as st
class DatabaseHandler():
    """ module to handle interactions with the database """

    def __init__(self) -> None:
        self.user = cfg.DATABASE_USER
        self.password = cfg.DATABASE_USER_PASSWORD
        self.database = cfg.DATABASE_NAME
        self.host = cfg.DATABASE_SERVICE
        self.connection = None
        self.review_columns = ", ".join(
                [
                    column.value if column.value != cfg.Reviews.ID.value \
                        else "" for column in cfg.Reviews
                ]
            )[1:]

    async def connect_to_database(self) -> bool:
        """ function to connect the database """
        self.connection = await apg.connect(
            user=self.user, password=self.password, database=self.database, host=self.host
        )
        if self.connection is not None:
            return True
        return False

    async def add_data(self, table_name: cfg.DatabaseTables, data: dict) -> None:
        """ function to add data to database """
        if table_name == cfg.DatabaseTables.REVIEWS:
            review_values = ", ".join(["'" + str(value) + "'" for value in data.values()])
            add_review = f"""
                INSERT INTO {cfg.DatabaseTables.REVIEWS.value}({self.review_columns}) VALUES ({review_values})
            """
            await self.connection.execute(add_review)

    async def remove_data(self, table_name: cfg.DatabaseTables, book_name: str) -> None:
        """ function to remove data from database """
        if table_name == cfg.DatabaseTables.REVIEWS:
            book_id = f"""
                SELECT {cfg.Books.ID.value} FROM {cfg.DatabaseTables.BOOKS.value}
                WHERE {cfg.Books.TITLE.value} = '{book_name}'
            """
            record = await self.connection.fetchrow(book_id)
            remove_review = f"""
                DELETE FROM {cfg.DatabaseTables.REVIEWS.value}
                WHERE {cfg.Reviews.BOOK_ID.value} = '{record[cfg.Books.ID.value]}'
                AND {cfg.Reviews.USER_ID.value} = '{cfg.USER_ID}'
            """
            await self.connection.execute(remove_review)

    async def get_all_books(self) -> dict:
        """ function to get all the available books """
        records = await self.connection.fetch(
            query=f"""SELECT * FROM {cfg.DatabaseTables.BOOKS.value}"""
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
            ON {cfg.DatabaseTables.BOOKS.value}.{cfg.Books.ID.value} = 
                {cfg.DatabaseTables.REVIEWS.value}.{cfg.Reviews.BOOK_ID.value}
            WHERE {cfg.DatabaseTables.BOOKS.value}.{cfg.Books.TITLE.value} = '{book_title}'
            """
        )
        return [
            (
                record[cfg.Reviews.USER_ID.value], record[cfg.Reviews.REVIEW.value]
            ) for record in records
        ]
