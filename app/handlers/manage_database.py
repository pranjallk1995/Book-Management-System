""" module to interact with the databse """

import config as cfg
import asyncpg as apg
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
                column.value for column in cfg.Reviews if column.value != cfg.Reviews.ID.value
            ]
        )
        self.book_columns = ", ".join(
            [
                column.value for column in cfg.Books if column.value != cfg.Books.ID.value
            ]
        )

    async def connect_to_database(self) -> bool:
        """ function to connect the database """
        self.connection = await apg.connect(
            user=self.user, password=self.password, database=self.database, host=self.host
        )
        if self.connection is not None:
            return True
        return False

    # ======================================================================================
    # Add/Remove specific data
    # ======================================================================================

    async def add_data(self, table_name: cfg.DatabaseTables, data: dict) -> None:
        """ function to add data to database """
        columns = None
        if table_name == cfg.DatabaseTables.REVIEWS:
            columns = self.review_columns
        elif table_name == cfg.DatabaseTables.BOOKS:
            columns = self.book_columns
        values = ", ".join(["'" + str(value) + "'" for value in data.values()])
        add_data = f"""
            INSERT INTO {table_name.value}({columns}) VALUES ({values})
        """
        await self.connection.execute(add_data)

    async def remove_data(self, table_name: cfg.DatabaseTables, book_title: str) -> None:
        """ function to remove data from database """
        if table_name == cfg.DatabaseTables.REVIEWS:
            book_id = await self.get_bookid(book_title)
            remove_review = f"""
                DELETE FROM {cfg.DatabaseTables.REVIEWS.value}
                WHERE {cfg.Reviews.BOOK_ID.value} = '{book_id}'
                AND {cfg.Reviews.USER_ID.value} = '{cfg.USER_ID}'
            """
            await self.connection.execute(remove_review)
        elif table_name == cfg.DatabaseTables.BOOKS:
            book_id = await self.get_bookid(book_title)
            remove_reviews = f"""
                DELETE FROM {cfg.DatabaseTables.REVIEWS.value}
                WHERE {cfg.Reviews.BOOK_ID.value} = '{book_id}'
            """
            await self.connection.execute(remove_reviews)
            remove_book = f"""
                DELETE FROM {cfg.DatabaseTables.BOOKS.value}
                WHERE {cfg.Books.TITLE.value} = '{book_title}'
            """
            await self.connection.execute(remove_book)

    # ======================================================================================
    # Get specific data
    # ======================================================================================

    async def get_review(self, book_title: str) -> apg.Record:
        """ function to get current user review """
        book_id = await self.get_bookid(book_title)
        return await self.connection.fetchrow(
            query=f"""
                SELECT * FROM {cfg.DatabaseTables.REVIEWS.value}
                WHERE {cfg.Reviews.USER_ID.value} = '{cfg.USER_ID}'
                AND {cfg.Reviews.BOOK_ID.value} = '{book_id}'
            """
        )

    async def get_bookid(self, book_tile: str) -> None:
        """ function to get the book id of the given book """
        records = await self.connection.fetch(
            query=f"""
                SELECT * FROM {cfg.DatabaseTables.BOOKS.value}
                WHERE {cfg.Books.TITLE.value} = '{book_tile}'
            """
        )
        return [record[cfg.Books.ID.value] for record in records][0]

    # ======================================================================================
    # Get all data
    # ======================================================================================

    async def get_all_books(self) -> dict:
        """ function to get all the available books """
        records = await self.connection.fetch(
            query=f"""SELECT * FROM {cfg.DatabaseTables.BOOKS.value}"""
        )
        return [record[cfg.Books.TITLE.value] for record in records]

    async def get_all_reviews(self, book_title: str) -> None:
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
