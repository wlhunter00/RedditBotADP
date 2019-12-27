# Imports
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Main function that runs everything
def main():
    info = openFile('loginInfo.txt')
    # reddit = loginReddit(info)
    # subreddit = loadSubreddit(reddit, info[5])
    loadGDrive(info[6])
    # parseComments(subreddit)


# Opening the file with the login info
def openFile(filename):
    fd = open(filename, 'r')
    file = fd.read()
    info = file.split(';')
    print(info)
    fd.close()
    return info


# Loging into reddit
def loginReddit(info):
    return praw.Reddit(user_agent=info[0],
                       client_id=info[1], client_secret=info[2],
                       username=info[3], password=info[4])


# load Subreddit
def loadSubreddit(reddit, subreddit):
    subreddit = reddit.subreddit(subreddit)


# Load Google drive
def loadGDrive(spreadsheet):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./client_secret.json', scope)
    client = gspread.authorize(creds)

    # Pick spreadsheet in the logininfo.txt
    sheet = client.open(spreadsheet).sheet1

    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)


# Parse the comments
def parseComments(subreddit):
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

if __name__ == "__main__":
    main()
