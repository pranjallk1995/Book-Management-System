""" module to interact with the databse """

import config as cfg

from utils.create_data import CreateData

class DatabaseHandler(CreateData):
    """ module to handle interactions with the database """

    def add_data(self, data: dict) -> None:
        """ function to add data to database """
        pass

    def remove_data(self, data: dict) -> None:
        """ function to remove data from database """
        pass

    async def get_all_books(self) -> dict:
        """ function to get all the available books """
        records = await self.connection.fetch(
            query=f"""SELECT * FROM {cfg.DatabaseTables.BOOKS.value}"""
        )
        return [record[cfg.Books.TITLE.value] for record in records]

    def get_book(self, book: str) -> None:
        """ function to get book details from database """
        pass

    def get_reviews(self, book: str) -> None:
        """ function to get reviews for the book from database """
        pass
