# Imports
import praw

# Opening the file with the login info
fd = open(r'loginInfo.txt', 'r')
file = fd.read()
info = file.split(';')
print(info)
fd.close()

reddit = praw.Reddit(user_agent=info[0],
                     client_id=info[1], client_secret=info[2],
                     username=info[3], password=info[4])

subreddit = reddit.subreddit('AskReddit')
# for submission in subreddit.stream.submissions():
for submission in subreddit.hot(limit=10):
    print("title: ", submission.title.encode("utf-8"))
    print("score: ", submission.score)
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        try:
            print("comment by ", comment.author.name.encode("utf-8"),
              ": ", comment.body.encode("utf-8"))
        except:
            print("error")
