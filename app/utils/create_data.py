""" module to create tables and its entries for first run """

import logging as lg
import config as cfg
import asyncpg as apg


class CreateData():
    """ create the bookstore database schema and book data """

    def __init__(self) -> None:
        self.user = cfg.DATABASE_USER
        self.password = cfg.DATABASE_USER_PASSWORD
        self.database = cfg.DATABASE_NAME
        self.host = cfg.DATABASE_SERVICE

    def check_status(self, status: str, table: cfg.DatabaseTables) -> None:
        """ check if creating table was successful """
        if "NOTICE" not in status:
            lg.info(" Table: %s has been created", table.value)
        elif "NOTICE" in status:
            lg.info(" Table: %s already exists", table.value)
        else:
            lg.error(" Failed to create Table: %s", table.value)

    async def create_tables(self) -> None:
        """ function to create tables if they do not exist """

        create_book_table = f"""
            CREATE TABLE IF NOT EXISTS {cfg.DatabaseTables.BOOKS.value}(
                id serial PRIMARY KEY,
                title varchar(255) NOT NULL,
                author varchar(255) NOT NULL,
                genre varchar(20),
                year_published DATE,
                summary varchar(8000),
                CONSTRAINT check_genre CHECK (genre IN ('Sports', 'Sci-Fi', 'Romance', 'Comedy', 'Drama', 'Action'))
            );
        """

        create_reviews_table = f"""
            CREATE TABLE IF NOT EXISTS {cfg.DatabaseTables.REVIEWS.value}(
                id serial PRIMARY KEY,
                book_id int,
                user_id int NOT NULL,
                review_text varchar(8000),
                rating int,
                FOREIGN KEY (book_id) REFERENCES books(id),
                CONSTRAINT check_rating CHECK (rating IN (1, 2, 3, 4, 5))
            );
        """

        connection = await apg.connect(
            user=self.user, password=self.password, database=self.database, host=self.host
        )

        create_status = await connection.execute(create_book_table)
        self.check_status(create_status, cfg.DatabaseTables.BOOKS)

        create_status = await connection.execute(create_reviews_table)
        self.check_status(create_status, cfg.DatabaseTables.REVIEWS)
