# -*- coding: utf-8 -*-
"""MySQL `TDT4145ProjectGroup131` database statements

This module contains code which defines the tables, their fields and their
constraints used to setup the `TDT4145ProjectGroup131` database. The database
name is stored in the string `DB_NAME` variable. The tables are stored in a dict
named `TABLES`.

"""

# Name of database
DB_NAME = "TDT4145ProjectGroup131"


# dict of the MySQL tables, their fields and their constraints.
# BINARY(16) types were used for IDs as they can store uuid.
TABLES = {}

# UserName was assumed to not necessarily be unique.
TABLES["User"] = (
    "CREATE TABLE `User` ("
    "  `UserID` binary(16) NOT NULL,"
    "  `UserName` varchar(100) NOT NULL,"
    "  `UserEmail` varchar(100) NOT NULL,"
    "  CONSTRAINT `User_PK` PRIMARY KEY (`UserID`),"
    "  CONSTRAINT `UserEmail_FK` UNIQUE KEY (`UserEmail`)"
    ") ENGINE=InnoDB"
)

# Password was assumed to not necessarily be unique.
TABLES["Login"] = (
    "CREATE TABLE `Login` ("
    "  `UserEmail` varchar(100) NOT NULL,"
    "  `Password` varchar(100) NOT NULL,"
    "  CONSTRAINT `Login_PK` PRIMARY KEY (`UserEmail`),"
    "  CONSTRAINT `Login_FK` FOREIGN KEY (`UserEmail`) REFERENCES `User` (`UserEmail`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

# CreatorType was assumed to not necessarily be unique.
TABLES["PostCreator"] = (
    "CREATE TABLE `PostCreator` ("
    "  `PCID` binary(16) NOT NULL,"
    "  `CreatorType` varchar(100) NOT NULL,"
    "  CONSTRAINT `PostCreator_PK` PRIMARY KEY (`PCID`)"
    ") ENGINE=InnoDB"
)

TABLES["Student"] = (
    "CREATE TABLE `Student` ("
    "  `StudentID` binary(16) NOT NULL,"
    "  `PCID` binary(16) NOT NULL,"
    "  CONSTRAINT `Student_PK` PRIMARY KEY (`StudentID`),"
    "  CONSTRAINT `PCID_UK1` UNIQUE KEY (`PCID`),"
    "  CONSTRAINT `Student_FK1` FOREIGN KEY (`StudentID`) REFERENCES `User` (`UserID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `Student_FK2` FOREIGN KEY (`PCID`) REFERENCES `PostCreator` (`PCID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["Instructor"] = (
    "CREATE TABLE `Instructor` ("
    "  `InstructorID` binary(16) NOT NULL,"
    "  `PCID` binary(16) NOT NULL,"
    "  CONSTRAINT `Instructor_PK` PRIMARY KEY (`InstructorID`),"
    "  CONSTRAINT `PCID_UK2` UNIQUE KEY (`PCID`),"
    "  CONSTRAINT `Instructor_FK1` FOREIGN KEY (`InstructorID`) REFERENCES `User` (`UserID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `Instructor_FK2` FOREIGN KEY (`PCID`) REFERENCES `PostCreator` (`PCID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

# Postcontent, PostType and PCID were assumed to not necessarily be unique.
TABLES["Post"] = (
    "CREATE TABLE `Post` ("
    "  `PostID` binary(16) NOT NULL,"
    "  `PostContent` varchar(500) NOT NULL,"
    "  `PCID` binary(16) NOT NULL,"
    "  `PostType` varchar(100) NOT NULL,"
    "  CONSTRAINT `Post_PK` PRIMARY KEY (`PostID`),"
    "  CONSTRAINT `Post_FK` FOREIGN KEY (`PCID`) REFERENCES `PostCreator` (`PCID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["UserLikesPost"] = (
    "CREATE TABLE `UserLikesPost` ("
    "  `UserID` binary(16) NOT NULL,"
    "  `PostID` binary(16) NOT NULL,"
    "  CONSTRAINT `UserLikesPost_PK` PRIMARY KEY (`UserID`, `PostID`),"
    "  CONSTRAINT `UserLikesPost_FK1` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `UserLikesPost_FK2` FOREIGN KEY (`PostID`) REFERENCES `Post` (`PostID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

# ThreadColor, StudentReplyID, and InstructorReplyID were assumed to not necessarily be unique.
# StudentReplyID and InstructorReplyID can be NULL.
TABLES["Thread"] = (
    "CREATE TABLE `Thread` ("
    "  `ThreadID` binary(16) NOT NULL,"
    "  `ThreadColor` int(10) NOT NULL,"
    "  `StudentReplyID` binary(16),"
    "  `InstructorReplyID` binary(16),"
    "  CONSTRAINT `Thread_PK` PRIMARY KEY (`ThreadID`),"
    "  CONSTRAINT `Thread_FK1` FOREIGN KEY (`StudentReplyID`) REFERENCES `Post` (`PostID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `Thread_FK2` FOREIGN KEY (`InstructorReplyID`) REFERENCES `Post` (`PostID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

# SuperPostID was assumed to not necessarily be unique.
TABLES["DiscussionPost"] = (
    "CREATE TABLE `DiscussionPost` ("
    "  `DiscussionPostID` binary(16) NOT NULL,"
    "  `SuperPostID` binary(16) NOT NULL,"
    "  `ThreadID` binary(16) NOT NULL,"
    "  CONSTRAINT `DiscussionPost_PK` PRIMARY KEY (`DiscussionPostID`),"
    "  CONSTRAINT `ThreadID_UK` UNIQUE KEY (`ThreadID`),"
    "  CONSTRAINT `DiscussionPost_FK1` FOREIGN KEY (`SuperPostID`) REFERENCES `DiscussionPost` (`DiscussionPostID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `DiscussionPost_FK2` FOREIGN KEY (`ThreadID`) REFERENCES `Thread` (`ThreadID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["Tags"] = (
    "CREATE TABLE `Tags` ("
    "  `ThreadID` binary(16) NOT NULL,"
    "  `Tag` varchar(100) NOT NULL,"
    "  CONSTRAINT `Tags_PK` PRIMARY KEY (`ThreadID`, `Tag`),"
    "  CONSTRAINT `Tags_FK` FOREIGN KEY (`ThreadID`) REFERENCES `Thread` (`ThreadID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

# CourseName, Term, PostAnonymity, and InvitationURL were assumed to not necessarily be unique.
TABLES["CourseForum"] = (
    "CREATE TABLE `CourseForum` ("
    "  `CourseID` binary(16) NOT NULL,"
    "  `CourseName` varchar(100) NOT NULL,"
    "  `Term` varchar(100) NOT NULL,"
    "  `PostAnonymity` boolean NOT NULL,"
    "  `InvitationURL` varchar(100) NOT NULL,"
    "  CONSTRAINT `CourseForum_PK` PRIMARY KEY (`CourseID`)"
    ") ENGINE=InnoDB"
)

TABLES["Folder"] = (
    "CREATE TABLE `Folder` ("
    "  `CourseID` binary(16) NOT NULL,"
    "  `FolderName` varchar(100) NOT NULL,"
    "  CONSTRAINT `Folder_PK` PRIMARY KEY (`CourseID`, `FolderName`),"
    "  CONSTRAINT `Folder_FK` FOREIGN KEY (`CourseID`) REFERENCES `CourseForum` (`CourseID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["ThreadInFolder"] = (
    "CREATE TABLE `ThreadInFolder` ("
    "  `ThreadID` binary(16) NOT NULL,"
    "  `CourseID` binary(16) NOT NULL,"
    "  `FolderName` varchar(100) NOT NULL,"
    "  CONSTRAINT `ThreadInFolder_PK` PRIMARY KEY (`ThreadID`, `CourseID`, `FolderName`),"
    "  CONSTRAINT `ThreadInFolder_FK1` FOREIGN KEY (`ThreadID`) REFERENCES `Thread` (`ThreadID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `ThreadInFolder_FK2` FOREIGN KEY (`CourseID`, `FolderName`) REFERENCES `Folder` (`CourseID`, `FolderName`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)


TABLES["UserViewsThread"] = (
    "CREATE TABLE `UserViewsThread` ("
    "  `UserID` binary(16) NOT NULL,"
    "  `ThreadID` binary(16) NOT NULL,"
    "  CONSTRAINT `UserViewsThread_PK` PRIMARY KEY (`UserID`, `ThreadID`),"
    "  CONSTRAINT `UserViewsThread_FK1` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `UserViewsThread_FK2` FOREIGN KEY (`ThreadID`) REFERENCES `Thread` (`ThreadID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)


TABLES["UserInCourse"] = (
    "CREATE TABLE `UserInCourse` ("
    "  `UserID` binary(16) NOT NULL,"
    "  `CourseID` binary(16) NOT NULL,"
    "  CONSTRAINT `UserInCourse_PK` PRIMARY KEY (`UserID`, `CourseID`),"
    "  CONSTRAINT `UserInCourse_FK1` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT `UserInCourse_FK2` FOREIGN KEY (`CourseID`) REFERENCES `CourseForum` (`CourseID`)"
    "          ON UPDATE CASCADE ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)
