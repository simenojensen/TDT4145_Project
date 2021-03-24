# -*- coding: utf-8 -*-
"""Code to create and fill `TDT4145ProjectGroup131` database with data.

This module contains code that creates the `TDT4145ProjectGroup131` database,
creates the tables of the `TDT4145ProjectGroup131` database, and fillss the
database with data found in the `.csv` files in `../data/`.

"""
import uuid
import sys
import pandas as pd
import numpy as np
from mysql import connector
from mysql.connector import errorcode


def create_database(cursor, DB_NAME):
    """Helper function to create database.

    Tries to create the database, prints and error and exists if unsuccessful.

    Parameters
    ----------
    cursor : :obj:
        The mysql.connector.cursor object used to execute MySQL queries.
    DB_NAME : str
        The MySQL database name (`TDT4145ProjectGroup131`)

    """
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except connector.Error as err:
        print("Failed creating database: {}".format(err))
        sys.exit(1)


def setup_database(user, password, DB_NAME, TABLES):
    """Function to setup database and tables.

    Drops the `TDT4145ProjectGroup131` database if already exists, then creates
    the database and executes the table initialization statements.

    Parameters
    ----------
    user : str
        The entered MySQL user.
    password : str
        The entered MySQL password.
    DB_NAME : str
        The MySQL database name (`TDT4145ProjectGroup131`).
    TABLES : dict
        A dict containing the tables and their MySQL statements. Used to set up
        the database with the correct tables.

    """

    # Instantiate connection
    with connector.connect(user=user, password=password) as cnx:

        # Instantiate cursor object
        with cnx.cursor() as cursor:
            # Start by dropping database
            try:
                cursor.execute("DROP DATABASE {}".format(DB_NAME))
            except connector.Error as err:
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database {} does not exists.".format(DB_NAME))
                else:
                    print(err.msg)
                    sys.exit(1)
            # Create database
            finally:
                create_database(cursor, DB_NAME)
                print("Database {} created successfully.".format(DB_NAME))
                # Set database tame
                cnx.database = DB_NAME

            # Create Tables if not exist
            for table_name in TABLES:
                table_description = TABLES[table_name]
                try:
                    print("Creating table {}: ".format(table_name), end="")
                    cursor.execute(table_description)
                except connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")


def insert_data(user, password, DB_NAME):
    """Insert data into MySQL database.

    Reads the `.csv` files from `../data/` and inserts the data into the
    existing `TDT4145ProjectGroup131` database.

    Parameters
    ----------
    user : str
        The entered MySQL user
    password : str
        The entered MySQL password
    DB_NAME : str
        The MySQL database name (`TDT4145ProjectGroup131`)

    """

    # Instantiate connection
    with connector.connect(user=user, password=password, database=DB_NAME) as cnx:

        # Instantiate cursor
        with cnx.cursor() as cursor:
            # Files need to be in read in order
            files = [
                "User.csv",
                "Login.csv",
                "PostCreator.csv",
                "Student.csv",
                "Instructor.csv",
                "CourseForum.csv",
                "Folder.csv",
                "UserInCourse.csv",
                "Post.csv",
                "UserLikesPost.csv",
                "Thread.csv",
                "UserViewsThread.csv",
                "Tags.csv",
                "ThreadInFolder.csv",
            ]

            for filename in files:
                # Get tablename
                tablename = filename.split(".")[0]

                print("Inserting into " + tablename + " : ", end="")

                # Load csv file
                table_df = pd.read_csv("../data/" + filename)
                # Replace nan with None as mysql convert None to NULL values
                table_df = table_df.replace({np.nan: None})

                # Replace string uuid values with uuid byte values
                for col in table_df.columns:
                    if "ID" in col:
                        table_df[col] = table_df[col].apply(
                            lambda x: uuid.UUID(x).bytes if isinstance(x, str) else x
                        )

                # Insert each row in df
                num_fails = 0
                for _, row in table_df.iterrows():
                    # Get a tuple of values to insert
                    to_insert = tuple(row[c] for c in table_df.columns)
                    # Adjust (%s, ..., %s) depending on number of column values to insert
                    string_tuple = "(" + "%s," * (len(table_df.columns) - 1) + "%s)"
                    # Create sql command for insertion
                    cmd = "INSERT INTO " + tablename + " VALUES " + string_tuple
                    # Insert into mysql database
                    try:
                        cursor.execute(cmd, to_insert)
                    except:
                        num_fails += 1

                if num_fails == 0:
                    print("Success")
                else:
                    print(f"Failed {num_fails} times")

                cnx.commit()
