# Imports
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import random


# Main function that runs everything
def main():
    info = openFile('loginInfo.txt')
    reddit = loginReddit(info)
    subreddit = loadSubreddit(reddit, info[5])
    listOfResponses = loadGDrive(info[6])
    parseComments(subreddit, listOfResponses, info[3])


# Opening the file with the login info and other info needed for the process.
# Input is name of file to scan.
# Returns information for main function.
def openFile(filename):
    fd = open(filename, 'r')
    file = fd.read()
    info = file.split(';')
    print(info)
    fd.close()
    return info


# Use regex to find if a phrase exists in the entire comment.
# Used by saying findWholeWord("Phrase")("Comment").
# Returns either the match object or null.
def findWholeWord(w):
    return re.compile(r'({0})'.format(w), flags=re.IGNORECASE).search


# Logging into reddit
# Input is information used for login.
# Returns a signed in reddit object
def loginReddit(info):
    return praw.Reddit(user_agent=info[0],
                       client_id=info[1], client_secret=info[2],
                       username=info[3], password=info[4])


# load Subreddit
# Inputs are the reddit and subreddit name
# Returns a subreddit
def loadSubreddit(reddit, subreddit):
    return reddit.subreddit(subreddit)


# Load Google drive and the sheet.
# To have the bot be able to access a file, share it with:
# "redditbot@reddit-bot-263322.iam.gserviceaccount.com"
# Input is the name of the spreadsheet.
# Returns a list of dictionarys, where column 1 is the comment,
# and column 2 is the response
def loadGDrive(spreadsheet):
    # Login to Google API using OAuth
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./client_secret.json', scope)
    client = gspread.authorize(creds)
    # Pick spreadsheet in the logininfo.txt
    sheet = client.open(spreadsheet).sheet1
    # Return pairs of comments and responses.
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)
    return list_of_hashes


# Parse the comments in a subreddit, if the comment has a phrase we are looking
# for, then respond with the matching response.
# With this setup, the stream.submissions() will have the bot always being
# Running, looking for any more inputs. Use subreddit.hot() or .new()
# to have it run one time.
def parseComments(subreddit, listOfResponses, botName):
    for submission in subreddit.stream.submissions():
        print("title: ", submission.title.encode("utf-8"))
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            for response in listOfResponses:
                if findWholeWord(response["Comment"])(comment.body):
                    alreadyCommented = False
                    if(comment.author.name != botName):
                        for secondCheck in comment.replies:
                            if(secondCheck.author.name == botName):
                                print("Bot already commented")
                                alreadyCommented = True
                                break
                        if not alreadyCommented:
                            responseName = "Response " + str(random.randint(1, response['Number of Responses']))
                            print("Match", response[responseName],
                                  comment.body.encode("utf-8"))
                            # comment.reply(response["Response"])
                    break


if __name__ == "__main__":
    main()
