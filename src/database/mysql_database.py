"""This Module provides all methods related for database operations"""
import os
import mysql.connector
import logging

from pathlib import Path
from dotenv import load_dotenv

from typing import Union
from database.database_query import CreateTablesQuery

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")


class Database:
    """
    This class contains method to perform all database related operations
    ...
    Methods
    -------
    init() : To create connection and cursor
    create_all_tables() : To create all the table
    save_data() : To save data in database
    fetch_data() : TO fetch data from database
    """

    connection = None
    cursor = None

    def __init__(self) -> None:
        """
        This method creates sqlite connection and cursor
        Parameters = self
        Return Type = None
        """
        if Database.connection is None:
            try:
                Database.connection = mysql.connector.connect(
                    user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST
                )
                CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {}"
                USE_DATABASE = "USE {}"
                Database.cursor = Database.connection.cursor(dictionary=True)
                Database.cursor.execute(CREATE_DATABASE.format(MYSQL_DB))
                Database.cursor.execute(USE_DATABASE.format(MYSQL_DB))
            except Exception as error:
                logger.exception(error)
                raise mysql.connector.Error from error
            else:
                logger.debug("Connection established")

        self.connection = Database.connection
        self.cursor = Database.cursor

    def create_all_table(self) -> None:
        """
        This method creates all tables of not exists
        Parameters = self
        Return Type = None
        """
        self.cursor.execute(CreateTablesQuery.query_create_user)
        self.cursor.execute(CreateTablesQuery.query_create_history)
        self.cursor.execute(CreateTablesQuery.query_create_message)
        self.cursor.execute(CreateTablesQuery.query_create_ban_url)
        self.cursor.execute(CreateTablesQuery.query_create_user_search)
        self.cursor.execute(CreateTablesQuery.query_create_premium_listing)

    def save_data(self, query: str, data: tuple) -> None:
        """
        This saves data in the database
        Parameters = query of type string, data are query parameters in tuple
        Return Type = None
        """
        self.cursor.execute(query, data)
        self.connection.commit()

    def fetch_data(self, query: str, tup: tuple = None) -> list:
        """
        This fetches data in the database
        Parameters = query, tuple
        Return Type = List
        """
        if not tup:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, tup)
        data = self.cursor.fetchall()
        return data


db = Database()
