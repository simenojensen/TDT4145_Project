# TDT4145_Project

**TDT4145_Project** is a Python implementation of the TDT4145 Project
Spring 2021. The program satisfies the listed

## Learning Outcomes
1. Get experience in data modelling and translation into SQL
2. Get practical experience in programming towards a SQL database using JDBC
3. Make concise documentation of high quality

## Use Cases
1. A student logs into the system, i.e., check user name and password (you do
   not need to encrypt/decrypt passwords). This should have e-mail and password
   as input, and these should match this info in the database.
2.  A student  makes a  post  belonging to  the  folder “Exam”  and tagged  with
   “Question”. Input to the  use case should be a post and  the texts “Exam” and
   “Question”.
3. An instructor replies to a post belonging to the folder “Exam”. The input to
   this is the id of the post replied to. This could be the post created in use
   case 2.
4. A student searches for posts with a specific keyword “WAL”. The return value
   of this should be a list of ids of posts matching the keyword.
5. An instructor views statistics for users and how many post they have read and
   how many they have created. These should be sorted on highest read posting
   numbers. The output is “user name, number of posts read, number of posts
   created”. You don’t need to order by posts created, but the number should be
   displayed. The result should also include users which have not read or
   created posts.
