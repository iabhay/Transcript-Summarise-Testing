"""This Module provides all methods related for database operations"""
import os
import pymysql
# import mysql.connector
import logging

from pathlib import Path
from dotenv import load_dotenv

from typing import Union
from database.database_query import CreateTablesQuery

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)

# MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
MYSQL_PASSWORD = '@Abhay6030'
# print(MYSQL_PASSWORD)
# MYSQL_HOST = os.getenv('DB_HOST')
MYSQL_HOST = 'localhost'
# MYSQL_DB = os.getenv('DB_DB')
MYSQL_PORT = 3306
# MYSQL_USERNAME = os.getenv('DB_USER')
MYSQL_USERNAME = 'root'

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
                timeout = 10
                Database.connection = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=timeout,
                cursorclass=pymysql.cursors.DictCursor,
                db="ytts",
                host=MYSQL_HOST,
                password=MYSQL_PASSWORD,
                read_timeout=timeout,
                port=int(MYSQL_PORT),
                user=MYSQL_USERNAME,
                write_timeout=timeout,
                )
                # Database.connection.autocommit(True)
                # CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {}"
                # USE_DATABASE = "USE {}"
                # ROLLBACK_QUERY = 'ROLLBACK'
                Database.cursor = Database.connection.cursor()
                # Database.cursor.execute(CREATE_DATABASE.format(MYSQL_DB))
                # Database.cursor.execute(USE_DATABASE.format(MYSQL_DB))
            except Exception as error:
                logger.exception(error)
            # else:
            #     logger.debug("Connection established")

        # self.connection = Database.connection

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
        self.cursor.execute(CreateTablesQuery.query_create_blocklist)

    def save_data(self, query: str, data: tuple) -> None:
        """
        This saves data in the database
        Parameters = query of type string, data are query parameters in tuple
        Return Type = None
        """
        print("In save data of history")
        print(query)
        print(data)
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
