""" module to access data from database """

import pandas as pd
import config as cfg
import asyncpg as apg


class LoadData():
    """ create the bookstore database schema and book data """

    def __init__(self) -> None:
        self.user = cfg.DATABASE_USER
        self.password = cfg.DATABASE_USER_PASSWORD
        self.database = cfg.DATABASE_NAME
        self.host = cfg.DATABASE_SERVICE
        self.connection = None

    async def get_dataframe(self, table_name: str) -> pd.DataFrame:
        """ function to return database data as a dataframe """

        self.connection = await apg.connect(
            user=self.user, password=self.password, database=self.database, host=self.host
        )
        records = await self.connection.fetch(f"SELECT * from {table_name};")
        records_dict = {}
        for index, record in enumerate(records):
            records_dict[index] = record
        database_dataframe = pd.DataFrame.from_dict(
            data=records_dict, orient="index", columns=["ID", "Title", "Author", "Genre", "Year", "Summary"]
        )
        return database_dataframe.drop(["ID"], axis=1)
