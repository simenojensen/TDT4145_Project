import uuid
import pandas as pd
import random

random.seed(6)
# random.seed(5)

foldernames = [
    "Ov1",
    "Ov2",
    "Ov3",
    "Ov4",
    "Project",
    "Exam",
    "Logistics",
    "Other",
    "Midterm",
    "Forelesninger",
    "Treningsoppgaver",
]


# User
user_df = pd.read_csv("../data/User.csv")
user_df['UserID'] = [str(uuid.uuid4()) for i in range(len(user_df))]
user_df.to_csv('../data/User.csv', index_label=False, index=False)

userid = user_df["UserID"].values.tolist()
studentid = random.sample(userid, 75)
instructorid = [i for i in userid if i not in studentid]


# Student
student_data = {
    "StudentID": studentid,
    "PCID": [str(uuid.uuid4()) for i in range(len(studentid))],
}
student_df = pd.DataFrame(data=student_data)
student_df.to_csv("../data/Student.csv", index_label=False, index=False)

# Instructor
instructor_data = {
    "InstructorID": instructorid,
    "PCID": [str(uuid.uuid4()) for i in range(len(instructorid))],
}
instructor_df = pd.DataFrame(data=instructor_data)
instructor_df.to_csv("../data/Instructor.csv", index_label=False, index=False)


# postcreator
student_df = pd.read_csv('../data/Student.csv')
instructor_df = pd.read_csv('../data/Instructor.csv')
postcreator_df = pd.DataFrame(columns=["PCID", "CreatorType"])
for pcid in student_df["PCID"].values:
    postcreator_df = postcreator_df.append(
        {"PCID": pcid, "CreatorType": "Student"}, ignore_index=True
    )
for pcid in instructor_df["PCID"].values:
    postcreator_df = postcreator_df.append(
        {"PCID": pcid, "CreatorType": "Instructor"}, ignore_index=True
    )
postcreator_df.to_csv("../data/PostCreator.csv", index_label=False, index=False)

# Login
user_df = pd.read_csv('../data/User.csv')
login_df = pd.read_csv("../data/Password.csv")
login_df = pd.concat([user_df["UserEmail"], login_df], axis=1)
login_df.to_csv("../data/Login.csv", index_label=False, index=False)

# CourseForm
course_df = pd.DataFrame(
    columns=["CourseID", "CourseName", "Term", "PostAnonymity", "InvitationURL"]
)
course_df = course_df.append(
    {
        "CourseID": str(uuid.uuid4()),
        "CourseName": "Datamodellering og Databaser",
        "Term": "Fall",
        "PostAnonymity": True,
        "InvitationURL": "https://piazza.com/class/kjip5mmtmj36o9",
    },
    ignore_index=True,
)
course_df.to_csv("../data/CourseForum.csv", index_label=False, index=False)

# Folder
course_df = pd.read_csv('../data/CourseForum.csv')
folder_df = pd.DataFrame(columns=["CourseID", "FolderName"])
courseid = course_df.at[0, "CourseID"]

for fn in foldernames:
    folder_df = folder_df.append(
        {"CourseID": courseid, "FolderName": fn}, ignore_index=True
    )
folder_df.to_csv("../data/Folder.csv", index_label=False, index=False)


# UserInCourse
userincourse_df = pd.DataFrame(columns=["UserID", "CourseID"])
user_df = pd.read_csv('../data/User.csv')
course_df = pd.read_csv('../data/CourseForum.csv')
for ind, row in user_df.iterrows():
    userincourse_df = userincourse_df.append(
        {"UserID": row["UserID"], "CourseID": course_df.at[0, "CourseID"]},
        ignore_index=True,
    )
userincourse_df.to_csv("../data/UserInCourse.csv", index_label=False, index=False)


# Post
post_df = pd.read_csv("../data/Post.csv")
# post_df = post_df.astype({'PostID':'object','PCID':'object'})
postcreator_df = pd.read_csv('../data/PostCreator.csv')
for ind, row in post_df.iterrows():
    pcid = random.sample(postcreator_df["PCID"].values.tolist(), 1)
    pcid = pcid[0]
    postid = str(uuid.uuid4())
    post_df.at[ind, "PostID"] = postid
    post_df.at[ind, "PCID"] = pcid
post_df.to_csv("../data/Post.csv", index_label=False, index=False)


# UserLikesPost
user_df = pd.read_csv('../data/User.csv')
post_df = pd.read_csv('../data/Post.csv')

userlikespost_df = pd.DataFrame(columns=["UserID", "PostID"])

userlike = random.choices(user_df["UserID"].values.tolist(), k=300)
userlikespost_df["UserID"] = userlike

postlike = random.choices(post_df["PostID"].values.tolist(), k=300)
userlikespost_df["PostID"] = postlike
userlikespost_df = userlikespost_df.drop_duplicates()
userlikespost_df.to_csv("../data/UserLikesPost.csv", index_label=False, index=False)


# Thread
thread_df = pd.DataFrame(
    columns=["ThreadID", "ThreadColor", "StudentReplyID", "InstructorReplyID"]
)
post_df = pd.read_csv('../data/Post.csv')
postcreator_df = pd.read_csv('../data/PostCreator.csv')
for ind, row in post_df.iterrows():
    if row["PostType"] == "Thread":
        # append thread post ids
        thread_df = thread_df.append({"ThreadID": row["PostID"]}, ignore_index=True)
    elif row["PostType"] == "Reply":
        # find which post reply is to
        threadid = post_df.iloc[ind - 1]["PostID"]
        threadind = thread_df.loc[thread_df["ThreadID"] == threadid].index[0]
        pcid = row["PCID"]
        # find what type the replier is either instructor or student
        replier = postcreator_df.loc[postcreator_df["PCID"] == pcid][
            "CreatorType"
        ].values
        if "Instructor" in replier:
            thread_df.at[threadind, "InstructorReplyID"] = row["PostID"]
        elif "Student" in replier:
            thread_df.at[threadind, "StudentReplyID"] = row["PostID"]

for ind, row in thread_df.iterrows():
    if isinstance(row["StudentReplyID"], str) and isinstance(
        row["InstructorReplyID"], str
    ):
        thread_df.at[ind, "ThreadColor"] = 3
    elif isinstance(row["StudentReplyID"], str):
        thread_df.at[ind, "ThreadColor"] = 2
    elif isinstance(row["InstructorReplyID"], str):
        thread_df.at[ind, "ThreadColor"] = 1
    else:
        thread_df.at[ind, "ThreadColor"] = 0

thread_df.to_csv("../data/Thread.csv", index_label=False, index=False)


# UserViewsThread
user_df = pd.read_csv('../data/User.csv')
thread_df = pd.read_csv('../data/Thread.csv')
userviewsthread_df = pd.DataFrame(columns=["UserID", "ThreadID"])
userview = random.choices(user_df["UserID"].values.tolist(), k=400)
threadview = random.choices(thread_df["ThreadID"].values.tolist(), k=400)
userviewsthread_df["UserID"] = userview
userviewsthread_df["ThreadID"] = threadview
userviewsthread_df = userviewsthread_df.drop_duplicates()
userviewsthread_df.to_csv("../data/UserViewsThread.csv", index_label=False, index=False)


# Discussion post

# Tags
tag_df = pd.DataFrame(columns=["ThreadID", "Tag"])
tags = [
    "Question",
    "Announcement",
    "Homework",
    "Homework Solution",
    "Lecture Notes",
    "General Announcement",
]

thread_df = pd.read_csv('../data/Thread.csv')
for ind, row in thread_df.iterrows():
    num = random.randint(0, 3)
    sample_tags = random.sample(tags, num)
    for tag in sample_tags:
        tag_df = tag_df.append(
            {"ThreadID": row["ThreadID"], "Tag": tag}, ignore_index=True
        )
tag_df.to_csv("../data/Tags.csv", index_label=False, index=False)




# Thread in folder
thread_df = pd.read_csv('../data/Thread.csv')
threadinfolder_df = pd.DataFrame(columns=["ThreadID", "CourseID", "FolderName"])
course_df = pd.read_csv('../data/CourseForum.csv')
courseid = course_df.at[0,'CourseID']
for ind, row in thread_df.iterrows():
    num = random.randint(1, 3)
    sample_folders = random.sample(foldernames, num)
    for fn in sample_folders:
        threadinfolder_df = threadinfolder_df.append(
            {"ThreadID": row["ThreadID"], "CourseID": courseid, "FolderName": fn},
            ignore_index=True,
        )
threadinfolder_df.to_csv("../data/ThreadInFolder.csv", index_label=False, index=False)
