# Imports
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import random


# Main function that runs everything
def main():
    info = openFile('C:\\Users\\William\\Documents\\GitHub\\RedditBotADP\\loginInfo.txt')
    reddit = loginReddit(info)
    subreddit = loadSubreddit(reddit, info[5])
    responses = loadGDrive(info[6], info[7])
    scrollSubreddit(subreddit, responses, info[3])


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
# Returns 2 lists of dictionaries, where column 1 is the comment/user being
# searched and column 2 is the response. The first element is number of
# dictionaries, the second element for comment parsing, the third for user.
def loadGDrive(spreadsheet, numberOfSheets):
    # Login to Google API using OAuth
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\William\\Documents\\GitHub\\RedditBotADP\\client_secret.json', scope)
    client = gspread.authorize(creds)
    # Do these twice, the first sheet being the comment parsing
    # The second sheet being user parsing
    spreadsheetOpen = client.open(spreadsheet)
    sheet1 = spreadsheetOpen.get_worksheet(0)
    commentParseResponses = sheet1.get_all_records()
    # Check in the loginInfo.txt document to see how many types of searches
    # are doing.
    if numberOfSheets == '2 sheets':
        sheet2 = spreadsheetOpen.get_worksheet(1)
        userParseResponses = sheet2.get_all_records()
        # If two, return a list of both dictionaries.
        return [2, commentParseResponses, userParseResponses]
    # Else return the one dictionary
    return [1, commentParseResponses]


# Parse the comments in a subreddit, if the comment has a phrase we are looking
# for, then respond with the matching response.
# With this setup, the stream.submissions() will have the bot always being
# Running, looking for any more inputs. Use subreddit.hot() or .new()
# to have it run one time.
def scrollSubreddit(subreddit, responses, botName):
    # Print responses from loadGDrive
    print(responses)
    # For each post in the subreddit
    for submission in subreddit.stream.submissions():
        print("title: ", submission.title.encode("utf-8"))
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            # Commented = False prevents a comment about the user and comment.
            commented = False
            # By default run the comment parser
            for response in responses[1]:
                # If a match
                if findWholeWord(response["Comment"])(comment.body):
                    # Respond to that comment
                    respondToComment(comment, response, botName)
                    commented = True
                    break
            # If the post hasn't been commented, and there is a
            # user sheet ready.
            if ((commented == False) and (responses[0] > 1)):
                for response in responses[2]:
                    # Checks usernames
                    if submission.author.name.lower() == response['Username'].lower():
                        # Respond to that comment
                        respondToComment(comment, response, botName)


# Respond to a comment
# Input is the comment object, the response object, and the name of the bot.
def respondToComment(comment, response, botName):
    # Check to make sure the bot isn't responding to itself.
    if(comment.author.name != botName):
        # Check the comment tree of replies for that comment to make sure that
        # The bot hasn't already said something. Done to prevent repeats.
        for secondCheck in comment.replies:
            if(secondCheck.author.name == botName):
                # If found just return and leave the function
                print("Bot already commented")
                return
        # if not already commented, randomly pick which response to choose from
        # This is done in the Number of Responses column in the google sheet.
        responseName = "Response " + str(random.randint(1, response['Number of Responses']))
        print("Match: Found -", comment.author.name, ":",
              comment.body.encode("utf-8"), "- Response:", response[responseName])
        comment.reply(response[responseName])


# Run main function
if __name__ == "__main__":
    main()
