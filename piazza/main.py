# -*- coding: utf-8 -*-
"""
TDT4145 Datamodellering og Databaser Project 2021
Author: Simen Omholt-Jensen, Anna Zhang, Vebjørn Steinsholt

This module contains code that runs the piazza interface.
"""
import sys
import getpass
from tables import TABLES
from tables import DB_NAME
from utils import setup_database
from utils import insert_data
from piazza_user import Student
from piazza_user import Instructor


def main():
    """Sets up the database and runs the program.

    Program prompts user for their MySQL login information. A database called
    `TDT4145ProjectGroup131` is created and filled with data from the `.csv`
    files in the `data` folder. Program is then run.

    """

    # Prompt the user for their MySQL login inforamtion
    user = input("Enter MySQL user: ")
    password = getpass.getpass(prompt="Enter MySQL password: ")

    # create piazza database
    setup_database(user, password, DB_NAME, TABLES)
    insert_data(user, password, DB_NAME)

    login_string = (
        "\nYou have three options:\n"
        "- Login as Student    [1]\n"
        "- Login as Instructor [2]\n"
        "- Quit                [q]"
    )

    while True:
        print(login_string)
        string = input("Please enter your option: ")
        if string == "1":
            student = Student(user, password, DB_NAME)
            student.close()
        elif string == "2":
            instructor = Instructor(user, password, DB_NAME)
            instructor.close()
        elif string.lower() == "q":
            print("\nBye!")
            sys.exit(0)
        else:
            print("Wrong option, try again")


if __name__ == "__main__":
    main()
