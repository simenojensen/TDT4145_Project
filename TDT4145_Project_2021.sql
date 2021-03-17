CREATE DATABASE IF NOT EXISTS Project;
USE Project;

-- BINARY(16) types were used for IDs as they can easily be generated in python.


-- UserName was assumed to not necessarily be unique.
CREATE TABLE IF NOT EXISTS User(
       UserID BINARY(16) NOT NULL,
       UserName VARCHAR(100) NOT NULL,
       UserEmail VARCHAR(100) NOT NULL,
       CONSTRAINT User_PK PRIMARY KEY (UserID),
       CONSTRAINT UserEmail_UK UNIQUE KEY (UserEmail)
);

-- Password was assumed to not necessarily be unique.
CREATE TABLE IF NOT EXISTS Login(
       UserEmail VARCHAR(100) NOT NULL,
       Password VARCHAR(100) NOT NULL,
       CONSTRAINT Login_PK PRIMARY KEY (UserEmail),
       CONSTRAINT Login_FK FOREIGN KEY (UserEmail) REFERENCES User(UserEmail)
               ON UPDATE CASCADE ON DELETE CASCADE
);

-- CreatorType was assumed to not necessarily be unique.
CREATE TABLE IF NOT EXISTS PostCreator(
       PCID BINARY(16) NOT NULL,
       CreatorType VARCHAR(100) NOT NULL,
       CONSTRAINT PostCreator_PK PRIMARY KEY (PCID)
);


CREATE TABLE IF NOT EXISTS Student(
       StudentID BINARY(16) NOT NULL,
       PCID BINARY(16) NOT NULL,
       CONSTRAINT Student_PK PRIMARY KEY (StudentID),
       CONSTRAINT PCID_UK1 UNIQUE KEY (PCID),
       CONSTRAINT Student_FK1 FOREIGN KEY (StudentID) REFERENCES User(UserID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT Student_FK2 FOREIGN KEY (PCID) REFERENCES PostCreator(PCID)
               ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Instructor(
       InstructorID BINARY(16) NOT NULL,
       PCID BINARY(16) NOT NULL,
       CONSTRAINT Instructor_PK PRIMARY KEY (InstructorID),
       CONSTRAINT PCID_UK2 UNIQUE KEY (PCID),
       CONSTRAINT Instructor_FK1 FOREIGN KEY (InstructorID) REFERENCES User(UserID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT Instructor_FK2 FOREIGN KEY (PCID) REFERENCES PostCreator(PCID)
               ON UPDATE CASCADE ON DELETE CASCADE
);

-- Postcontent and PostType were assumed to not necessarily be unique.
CREATE TABLE IF NOT EXISTS Post(
       PostID BINARY(16) NOT NULL,
       PostContent VARCHAR(500) NOT NULL,
       PCID BINARY(16) NOT NULL,
       PostType VARCHAR(100) NOT NULL,
       CONSTRAINT Post_PK PRIMARY KEY (PostID),
       CONSTRAINT PCID_UK3 UNIQUE KEY (PCID),
       CONSTRAINT Post_FK FOREIGN KEY (PCID) REFERENCES PostCreator(PCID)
               ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserLikesPost(
       PostID BINARY(16) NOT NULL,
       UserID BINARY(16) NOT NULL,
       CONSTRAINT UserLikesPost_PK PRIMARY KEY (PostID, UserID),
       CONSTRAINT UserLikesPost_FK1 FOREIGN KEY (PostID) REFERENCES Post(PostID)
               ON DELETE CASCADE ON UPDATE CASCADE,
       CONSTRAINT UserLikesPost_FK2 FOREIGN KEY (UserID) REFERENCES User(UserID)
               ON DELETE CASCADE ON UPDATE CASCADE
);

-- ThreadColor, StudentReplyID, and InstructorReplyID were assumed to not necessarily be unique.
-- StudentReplyID and InstructorReplyID can be NULL.
CREATE TABLE IF NOT EXISTS Thread(
       ThreadID BINARY(16) NOT NULL,
       ThreadColor INT(10) NOT NULL,
       StudentReplyID BINARY(16),
       InstructorReplyID BINARY(16),
       CONSTRAINT Thread_PK PRIMARY KEY (ThreadID),
       CONSTRAINT Thread_FK1 FOREIGN KEY (StudentReplyID) REFERENCES Post(PostID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT Thread_FK2 FOREIGN KEY (InstructorReplyID) REFERENCES Post(PostID)
               ON UPDATE CASCADE ON DELETE CASCADE
);

-- SuperPostID was assumed to not necessarily be unique.
CREATE TABLE IF NOT EXISTS DiscussionPost(
       DiscussionPostID BINARY(16) NOT NULL,
       SuperPostID BINARY(16) NOT NULL,
       ThreadID BINARY(16) NOT NULL,
       CONSTRAINT DiscussionPost_PK PRIMARY KEY (DiscussionPostID),
       CONSTRAINT ThreadID_UK UNIQUE KEY (ThreadID),
       CONSTRAINT DiscussionPost_FK1 FOREIGN KEY (SuperPostID) REFERENCES DiscussionPost(DiscussionPostID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT DiscussionPost_FK2 FOREIGN KEY (ThreadID) REFERENCES Thread(ThreadID)
               ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Tags(
       ThreadID BINARY(16) NOT NULL,
       Tag VARCHAR(100) NOT NULL,
       CONSTRAINT Tags_PK PRIMARY KEY (ThreadID, Tag),
       CONSTRAINT Tags_FK FOREIGN KEY (ThreadID) REFERENCES Thread(ThreadID)
               ON DELETE CASCADE ON UPDATE CASCADE
);

-- CourseName, Term, PostAnonymity, and InvitationURL were assumed to not necessarily be unique.
CREATE TABLE IF NOT EXISTS CourseForum(
       CourseID BINARY(16) NOT NULL,
       CourseName VARCHAR(100) NOT NULL,
       Term VARCHAR(100) NOT NULL,
       PostAnonymity BOOLEAN NOT NULL,
       InvitationURL VARCHAR(100) NOT NULL,
       CONSTRAINT CourseForum_PK PRIMARY KEY (CourseID)
);

CREATE TABLE IF NOT EXISTS Folder(
       CourseID BINARY(16) NOT NULL,
       FolderName VARCHAR(100) NOT NULL,
       CONSTRAINT Folder_PK PRIMARY KEY (CourseID, FolderName),
       CONSTRAINT Folder_FK FOREIGN KEY (CourseID) REFERENCES CourseForum(CourseID)
               ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ThreadInFolder(
       ThreadID BINARY(16) NOT NULL,
       CourseID BINARY(16) NOT NULL,
       FolderName VARCHAR(100) NOT NULL,
       CONSTRAINT ThreadInFolder_PK PRIMARY KEY (ThreadID, CourseID, FolderName),
       CONSTRAINT ThreadInFolder_FK1 FOREIGN KEY (ThreadID) REFERENCES Thread(ThreadID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT ThreadInFolder_FK2 FOREIGN KEY (CourseID, FolderName) REFERENCES Folder(CourseID, FolderName)
               ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserViewsThread(
       UserID BINARY(16) NOT NULL,
       ThreadID BINARY(16) NOT NULL,
       CONSTRAINT UserViewsThread_PK PRIMARY KEY (UserID, ThreadID),
       CONSTRAINT UserViewsThread_FK1 FOREIGN KEY (UserID) REFERENCES User(UserID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT UserViewsThread_FK2 FOREIGN KEY (ThreadID) REFERENCES Thread(ThreadID)
               ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS UserInCourse(
       UserID BINARY(16) NOT NULL,
       CourseID BINARY(16) NOT NULL,
       CONSTRAINT UserInCourse_PK PRIMARY KEY (UserID, CourseID),
       CONSTRAINT UserInCourse_FK1 FOREIGN KEY (UserID) REFERENCES User(UserID)
               ON UPDATE CASCADE ON DELETE CASCADE,
       CONSTRAINT UserInCourse_FK2 FOREIGN KEY (CourseID) REFERENCES CourseForum(CourseID)
               ON UPDATE CASCADE ON DELETE CASCADE
);
