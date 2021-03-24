# -*- coding: utf-8 -*-
"""Classes containing functionality for the required use cases.

This module contains code for the classes implementing the functionality for the
required use cases. The PiazzaUser class is a superclass to the Instructor and
Student classes. The PiazzaUser contains functionality shared between the
Instructor and Student classes such as logging in, creating posts such as
threads or replies, and keyword search. The Instructor classes includes
functionality for viewing statistics.

"""
import uuid
import getpass
from mysql import connector
from prettytable import PrettyTable


class PiazzaUser:
    """Class for login, post creation and keyword search functionality.

    This class includes functionality for setting up a MySQL connection to the
    `TDT4145ProjectGroup131` database, loggin into the Piazza interface,
    creating different types of posts such as threads and replies, and keyword
    search among posts in the database.

    Attributes
    ----------
    cnx : :obj:
        The mysql.connector object used to establish a connection to the MySQL
        database.
    userid : str
        The retrieved UserID from successful login attempt.
    courseid : str
        The retrieved CourseID from successful login attempt.
    pcid : str
        The retrieved PCID from successful login attempt.
    """

    def __init__(self, user, password, DB_NAME):
        """Set up MySQL connection and call login function

        Parameters
        ----------
        user : str
            The entered MySQL user.
        password : str
            The entered MySQL password.
        DB_NAME : str
            The MySQL database name (`TDT4145ProjectGroup131`).

        """
        self.cnx = connector.connect(user=user, password=password, database=DB_NAME)
        self.login()

    def login(self):
        """Verify UserEmail and Password to let user log in.

        Prompts the user for their email and password. If the information exists
        in the `TDT4145ProjectGroup131` database, retrieve user specific
        information such as UserID, CourseID, and PCID.

        Example
        -------
        Student:
            # useremail = "frumford6@ted.com"
            # userpassword = "XpdsDP085Un"
        Instructor:
            # useremail = "stretters@mashable.com"
            # userpassword = "AQqzBO2mTEkB"

        """
        while True:
            useremail = input("\nPlease enter email: ")
            args = (useremail,)
            with self.cnx.cursor() as cursor:
                cmd = "SELECT * FROM Login WHERE UserEmail= %s"
                cursor.execute(cmd, args)
                result = cursor.fetchall()

            if result:
                userpassword = getpass.getpass(prompt="Please enter password: ")
                args = (useremail, userpassword)
                with self.cnx.cursor() as cursor:
                    cmd = (
                        "SELECT * FROM Login "
                        "WHERE UserEmail = %s AND Password = %s"
                    )
                    cursor.execute(cmd, args)
                    result = cursor.fetchall()

                if result:
                    # Get User ID
                    with self.cnx.cursor() as cursor:
                        cmd = (
                            "SELECT BIN_TO_UUID(UserID) FROM User "
                            "WHERE UserEmail = %s"
                        )
                        args = (useremail,)
                        cursor.execute(cmd, args)
                        result = cursor.fetchall()
                        self.userid = result[0][0]

                    # Check if user is instructor or student
                    if isinstance(self, Student):
                        cmd = (
                            "SELECT BIN_TO_UUID(StudentID) FROM Student "
                            "WHERE BIN_TO_UUID(StudentID)=%s"
                        )
                    else:
                        assert isinstance(self, Instructor)
                        cmd = (
                            "SELECT BIN_TO_UUID(InstructorID) "
                            "FROM Instructor "
                            "WHERE BIN_TO_UUID(InstructorID)=%s"
                        )
                    with self.cnx.cursor() as cursor:
                        args = (self.userid,)
                        cursor.execute(cmd, args)
                        result = cursor.fetchall()

                    if result:
                        # Get courseID
                        with self.cnx.cursor() as cursor:
                            cmd = (
                                "SELECT BIN_TO_UUID(CourseID) "
                                "FROM UserInCourse "
                                "WHERE BIN_TO_UUID(UserID)=%s"
                            )
                            args = (self.userid,)
                            cursor.execute(cmd, args)
                            result = cursor.fetchall()
                            self.courseid = result[0][0]

                        # Get student or instructor pcid
                        if isinstance(self, Student):
                            cmd = (
                                "SELECT BIN_TO_UUID(PCID) "
                                "FROM Student "
                                "WHERE BIN_TO_UUID(StudentID)=%s"
                            )
                        else:
                            assert isinstance(self, Instructor)
                            cmd = (
                                "SELECT BIN_TO_UUID(PCID) "
                                "FROM Instructor "
                                "WHERE BIN_TO_UUID(InstructorID)=%s"
                            )
                        with self.cnx.cursor() as cursor:
                            args = (self.userid,)
                            cursor.execute(cmd, args)
                            result = cursor.fetchall()
                            self.pcid = result[0][0]
                        return

                    if isinstance(self, Student):
                        print("You are not a Student!")
                    else:
                        print("You are not an Instructor!")
                else:
                    print("Incorrect password")
            else:
                print("Email not in database")

    def create_post(self):
        """Prompt user for post creation details

        User can create a thread, a reply, or go back.
        """

        create_post_string = (
            "\n\nYou have three options:\n"
            "- Create a thread       [1]\n"
            "- Create a reply        [2]\n"
            "- Go back               [q]\n"
        )

        while True:
            print(create_post_string)
            post_string = input("Please enter your option: ")
            if post_string == "1":
                self.create_thread()
            elif post_string == "2":
                self.create_reply()
            elif post_string.lower() == "q":
                return
            else:
                print("Wrong option, try again")

    def create_thread(self):
        """Execute MySQL quries necessary for thread creation.

        Prompt the user for post content, folder, and tag. Then update the
        `TDT4145ProjectGroup131` database by inserting new data into the `Post`,
        `Thread`, `Tags`, and `ThreadInFolder` tables.

        """
        postcontent = input("Please enter your post content: ")
        folder = input("Please enter your post folder: ")
        tag = input("Please enter your post tag: ")

        # Insert into Post
        with self.cnx.cursor() as cursor:
            cmd = "INSERT INTO Post VALUES(%s, %s, %s, 'Thread')"
            # Genereate postid
            postid = uuid.uuid4()
            print(f"\nPostID of created post: {str(postid)}")
            postid = postid.bytes
            pcid = uuid.UUID(self.pcid).bytes
            args = (postid, postcontent, pcid)
            cursor.execute(cmd, args)
            self.cnx.commit()

        # Insert into Thread
        with self.cnx.cursor() as cursor:
            # New thread gets 0 as colorcode, and NULL values for reply fields.
            cmd = "INSERT INTO Thread VALUES(%s, 0, NULL, NULL)"
            args = (postid,)
            cursor.execute(cmd, args)
            self.cnx.commit()

        # Insert into Tags
        with self.cnx.cursor() as cursor:
            cmd = "INSERT INTO Tags VALUES(%s, %s)"
            args = (postid, tag)
            cursor.execute(cmd, args)
            self.cnx.commit()

        # Insert into ThreadInFolder
        with self.cnx.cursor() as cursor:
            cmd = "INSERT INTO ThreadInFolder VALUES(%s, %s, %s)"
            courseid = uuid.UUID(self.courseid).bytes
            args = (postid, courseid, folder)
            cursor.execute(cmd, args)
            self.cnx.commit()

    def create_reply(self):
        """Execute MySQL quries necessary for reply creation.

        Prompt the user for the id of the post to reply to and post
        content. Then update the `TDT4145ProjectGroup131` database by inserting
        new data into the `Post` table, and update the `Thread` table.

        """
        while True:
            postreplyid = input("Please enter id of post to reply to: ")
            postcontent = input("Please enter your post content: ")

            # check to see if entered postid is valid
            with self.cnx.cursor() as cursor:
                cmd = (
                    "SELECT BIN_TO_UUID(PostID) FROM Post "
                    "WHERE BIN_TO_UUID(PostID)=%s"
                )
                args = (postreplyid,)
                cursor.execute(cmd, args)
                result = cursor.fetchall()
            if result:
                # Insert into Post table
                with self.cnx.cursor() as cursor:
                    cmd = "INSERT INTO Post VALUES(%s, %s, %s, 'Reply')"
                    # generate reply postid
                    replyid = uuid.uuid4().bytes
                    pcid = uuid.UUID(self.pcid).bytes
                    args = (replyid, postcontent, pcid)
                    cursor.execute(cmd, args)
                    self.cnx.commit()

                # Update Thread table
                with self.cnx.cursor() as cursor:
                    cmd = (
                        "UPDATE Thread "
                        "SET InstructorReplyID=%s, Threadcolor=13 "
                        "WHERE ThreadID=%s"
                    )
                    postreplyid_b = uuid.UUID(postreplyid).bytes
                    args = (replyid, postreplyid_b)
                    cursor.execute(cmd, args)
                    self.cnx.commit()
                return
            print("Wrong post id")

    def search_keyword(self):
        """Let user search the database for a keyword.

        The search functionality contains (1) search for keyword in post
        content, (2) search for keyword in thread tags, (3) search for keyword
        in folder names, and (4) search for keyword in user name. The search
        returns PostIDs for posts related to the above searches. First prompt
        the user for a keyword, then print list of returned PostIDs.

        """
        keyword = input("Please enter keyword: ")
        keyword = "%" + keyword + "%"
        with self.cnx.cursor() as cursor:
            cmd = (
                "SELECT BIN_TO_UUID(PostID) FROM Post "
                "WHERE PostContent LIKE %s"
            )
            args = (keyword,)
            cursor.execute(cmd, args)
            result1 = cursor.fetchall()
            result1 = [t[0] for t in result1]

        with self.cnx.cursor() as cursor:
            cmd = (
                "SELECT BIN_TO_UUID(ThreadID) FROM Tags "
                "WHERE Tag LIKE %s"
            )
            args = (keyword,)
            cursor.execute(cmd, args)
            result2 = cursor.fetchall()
            result2 = [t[0] for t in result2]

        with self.cnx.cursor() as cursor:
            cmd = (
                "SELECT BIN_TO_UUID(ThreadID) FROM ThreadInFolder "
                "INNER JOIN "
                "(SELECT * FROM Folder "
                "WHERE FolderName LIKE %s) AS T1 "
                "USING (CourseID, FolderName);"
            )
            args = (keyword,)
            cursor.execute(cmd, args)
            result3 = cursor.fetchall()
            result3 = [t[0] for t in result3]

        with self.cnx.cursor() as cursor:
            cmd = (
                "SELECT BIN_TO_UUID(PostID) FROM Post "
                "INNER JOIN "
                "(SELECT PCID FROM Student INNER JOIN "
                "(SELECT UserID FROM User WHERE UserName LIKE %s) AS U1 "
                "ON (UserID=StudentID) "
                "UNION "
                "SELECT PCID FROM Instructor INNER JOIN "
                "(SELECT UserID FROM User WHERE UserName LIKE %s) AS U2 "
                "ON (UserID=InstructorID)) AS T1 "
                "USING(PCID);"
            )
            args = (keyword, keyword)
            cursor.execute(cmd, args)
            result4 = cursor.fetchall()
            result4 = [t[0] for t in result4]

        result = result1 + result2 + result3 + result4
        # Only unique items
        result = list(set(result))
        # Print nice table
        print("Here are your search results:")
        table = PrettyTable()
        table.field_names = ["PostID"]
        for i in result:
            table.add_row([i])
        print(table)

    def close(self):
        """Close the MySQL connection.
        """
        self.cnx.close()


class Student(PiazzaUser):
    """Class for student login.

    This class includes an interface for the logged in students.

    """

    def __init__(self, user, password, DB_NAME):
        """Call the PiazzaUser __init__ and Student action_menu functions.

        Parameters
        ----------
        user : str
            The entered MySQL user.
        password : str
            The entered MySQL password.
        DB_NAME : str
            The MySQL database name (`TDT4145ProjectGroup131`).

        """
        super().__init__(user, password, DB_NAME)
        self.action_menu()

    def action_menu(self):
        """Student action menu interface.

        A student can make a post, search for a keyword or log out.
        """
        action_menu_string = (
            "\n\nYou have three options:\n"
            "- Make a post            [1]\n"
            "- Search for a keyword   [2]\n"
            "- Log out                [q]\n"
        )

        while True:
            print(action_menu_string)
            action_string = input("Please enter your option: ")
            if action_string == "1":
                self.create_post()
            elif action_string == "2":
                self.search_keyword()
            elif action_string.lower() == "q":
                return
            else:
                print("Wrong option, try again")


class Instructor(PiazzaUser):
    """Class for Instructor login.

    This class includes an interface for the logged in instructors, and
    functionality for viewing post statistics.

    """

    def __init__(self, user, password, DB_NAME):
        """Call the PiazzaUser __init__ and Instructor action_menu functions.

        Parameters
        ----------
        user : str
            The entered MySQL user.
        password : str
            The entered MySQL password.
        DB_NAME : str
            The MySQL database name (`TDT4145ProjectGroup131`).

        """
        super().__init__(user, password, DB_NAME)
        self.action_menu()

    def action_menu(self):
        """Instructior action menu interface.

        An instructor can make a post, search for a keyword, view statistics or
        log out.

        """
        action_menu_string = (
            "\n\nYou have four options:\n"
            "- Make a post            [1]\n"
            "- Search for a keyword   [2]\n"
            "- View Statistics        [3]\n"
            "- Log out                [q]\n"
        )

        while True:
            print(action_menu_string)
            action_string = input("Please enter your option: ")
            if action_string == "1":
                self.create_post()
            elif action_string == "2":
                self.search_keyword()
            elif action_string == "3":
                self.view_statistics()
            elif action_string.lower() == "q":
                return
            else:
                print("Wrong option, try again")

    def view_statistics(self):
        """Print thread views and post creation statistics.

        Print the usernames, numberOfThreadsRead, and numberOfPostsCreated.
        """
        with self.cnx.cursor() as cursor:
            cmd = (
                "SELECT UserName, "
                "NumberOfThreadsRead, "
                "NumberOfPostscreated "
                "FROM User "
                "INNER JOIN "
                "(SELECT UserID, "
                "NumberOfThreadsRead, "
                "NumberOfPostsCreated "
                "FROM "
                "(SELECT UserID, "
                "COUNT(PostID) AS NumberOfPostsCreated "
                "FROM "
                "(SELECT UserID, "
                "PCID "
                "FROM User "
                "INNER JOIN Student ON (UserID=StudentID) "
                "UNION SELECT UserID, "
                "PCID "
                "FROM User "
                "INNER JOIN Instructor ON (UserID=InstructorID)) AS T1 "
                "LEFT OUTER JOIN Post USING (PCID) "
                "GROUP BY (UserID)) AS T2 "
                "INNER JOIN "
                "(SELECT Userid, "
                "COUNT(ThreadID) AS NumberOfThreadsRead "
                "FROM User "
                "LEFT OUTER JOIN UserViewsThread USING (UserID) "
                "GROUP BY (UserID)) AS T3 USING (UserID)) AS T4 USING (UserID) "
                "ORDER BY NumberOfThreadsRead DESC"
            )

            cursor.execute(cmd)
            result = cursor.fetchall()

        table = PrettyTable()
        table.field_names = [
            "UserName",
            "NumberOfThreadsRead",
            "NumberOfPostsCreated",
        ]
        table.align["UserName"] = "l"
        table.align["NumberOfThreadsRead"] = "r"
        table.align["NumberOfPostsCreated"] = "r"
        for row in result:
            table.add_row(list(row))
        print(table)
