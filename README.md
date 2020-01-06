# RedditBotADP
## Introduction
This is a reddit bot that I created that will parse through all of the comments in a subreddit, and reply to them based on certain keywords or certain users that did the commenting. The list of users and words to look for are stored within a Google Sheets document. The bot finds matches using Regular Expressions. This bot can be scaled to look for many different things in the comment, such as comment score, and the type of reply can also be scaled to be more complex.

This reddit bot can be used for any subreddit, and look for any words/users. It can be scaled however the user my want it.

#### Process
1. Load all information needed from a text document.
2. Login to Reddit's API based on credentials given.
3. Load the subreddit that we want to look at.
4. Login to Google Drive's API and pull up the spreadsheet that we want to look at. Put all the information from the two (or one) workbooks into objects, and return them.
5. Go through every post in the subreddit and look through it's comments. Parse each comment to see if it has any of the keywords that we are looking for.
6. If there is a match, then check to see if the Bot was the one that commented, or if that bot has ever responded in that chain. Then it will reply to the comment.
7. Check to see the username of the commenter. If it is in the list of users we want to reply to, go to step 6.

## Table of Contents
* [Introduction](#introduction)
* [Table of Contents](#table-of-contents)
* [Project Status](#project-status)
  * [Recently added](#recently-added)
  * [To Do](#to-do)
  * [Bugs](#bugs)
* [Technologies](#technologies)
* [Installation](#installation)
  * [Setting up Python](#setting-up-python)
  * [Setting up with Reddit](#setting-up-with-reddit)
  * [Setting up with Google](#setting-up-with-google)
  * [Preparing Login Info](#preparing-logininfo)
* [Walkthroughs](#Walkthroughs)
  * [Functions Walkthrough](#functions-walkthrough)
  * [Text file Walkthrough](#textfile-walkthrough)
  * [Spreadsheet Walkthrough](#spreadsheet-walkthrough)

## Project Status
###### **Version 1.0.2**

Stable build is currently ready.

##### **Recently Added**
- [X] Created this README as a guide to the application.
- [X] Allowed for users to be parsed

#### To Do:
- [ ] Allow the responses from the bot to interact with the comment.
- [ ] Create "Smart" responses that can answer questions.
- [ ] Allow the option to search multiple subreddits at once.

#### Bugs:
- No bugs found yet.

## Technologies
Project was created with:
- Python Version: 3.7
  - Praw
  - Gspread
  - OAuth2
  - Regex
- Regular Expressions
- Google Sheets

## Installation
### Setting Up Python
First, you  need to install [Python 3.7.1](https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe) (you need to have a python version 3.0+). I use [ATOM](https://atom.io/download/windows_x64) as my text editor, by any works.

Then you are going to set your PATH and ```python -m pip install``` in the command prompt the following libraries:

1. praw
2. gspread
3. oauth2client

### Setting up with Reddit
You will then need to connect to a reddit account. Consider this [webpage](https://praw.readthedocs.io/en/v3.6.0/pages/oauth.html) on how to setup your "application" with reddit. I am not putting out my personal details for my bot account.

### Setting up with Google
Then you will want to create a secret key with Google's API to gain access to Google Drive. (Obtained from [Twilio](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html))
1. Go to [Google's APIs Console](https://console.developers.google.com/)
2. Create a new project.
3. Click Enable API. Search for and enable the Google Drive API.
4. Create credentials for a Web Server to access Application Data.
5. Name the service account and grant it a Project Role of Editor.
6. Download the JSON file.
7. Copy the JSON file to your code directory and rename it to client_secret.json
8. Go into client_secret.json, and find the 'client_email'. Copy the email and share it to the sheet you want to access.

### Preparing Login Info
You will then need to create a **loginInfo.txt** document. It should be structured like so:

Reddit userAgent;reddit client_id;reddit client_secret;reddit account username;reddit account password;subreddit you want to parse;Spreadsheet name;Number of Sheets.

#### Example:

script: Response Bot:v1.0.2:(by /u/wlhunter00);client_id;client_scrent;BotName123;Password123;AskReddit;Bot Responses;2 sheets;

The lack of spaces between the semicolons are very important.

Look at [Text file Walkthrough](#textfile-walkthrough) for more details on what that document operates.

## Walkthroughs

### Functions Walkthrough:
- ```def main():``` The main function of the script that will call all the important functions and complete the process.
  - Parameters: None.
  - Returns: Nothing.
  - Called by: First run of script.
- ```def openFile(filename):``` Opens up a text file (loginInfo.txt) and returns the information.
  - Parameters: Name of the file with the information
  - Returns: Array of strings with the given information.
  - Called by: ```main()```.
- ```def findWholeWord(w):``` Using regex to find if a phrase exists in the entire comment. Used by saying findWholeWord("Phrase")("Comment").
  - Parameters: The phrase we are looking for.
  - Returns: Either with a match object or None.
  - Called by ```scrollSubreddit()```.
- ```def loginReddit():``` Logs in to reddit's API.
  - Parameters: Login information from the text file.
  - Returns: The reddit object.
  - Called by: ```main():```.
- ```def loadSubreddit(reddit, subreddit):``` Loads a subreddit.
  - Parameters: The reddit object from loginReddit, and a string of the subreddits name, found in loginInfo.txt
  - Returns: The subreddit object.
  - Called by: ```main()```.
- ```def loadGDrive(spreadsheet, numberOfSheets):``` Logins in to the Google Drive APi. Opens up the spreadsheet, and loads the two workbook pages into objects.
  - Parameters: Spreadsheet name as a string, and the number of sheets. Both of this is from loginInfo.txt
  - Returns: Returns a list. The first object in the list is the number of sheets that were scraped. The second object will be all of the information regarding the comment scraping. It is stored so that it is an array with a comment (key) and responses.
  - Called by: ```main()```.
- ```def scrollSubreddit(subreddit, responses, botName):``` Goes through the subreddit and pulls all the comments, then checks to see if the comments are a match.
  - Parameters: The subreddit object, the responses object from loadGDrive, and the name of the boat.
  - Returns: None.
  - Called by: ```main()```.
- ```def respondToComment(comment, response, botName):``` Checks to see if the bot should reply to the comment, then replys to the comment.
  - Parameters: The comment object we are looking at, the response object, and the name of the bot.
  - Returns: None.
  - Called by: ```def scrollSubreddit()```.

### Text File Walkthrough:
You will need to create two text files for the bot to work, as I have both of them in my .gitignore. The first is loginInfo.txt and the second is client_secret.json

loginInfo.txt must be set up as mentioned in [Preparing Login Info](#preparing-logininfo). The ```def openFile()``` method breaks up the information from the file as so:

- info[0] is the user_agent for reddit.
- info[1] is the client_id for reddit.
- info[2] is the client_secret for reddit.
- info[3] is the username of the reddit account.
- info[4] is the password of the reddit account.
- info[5] is the name of the subreddit we want to look at.
- info[6] is the name of the google spreadsheet we want to open.
- info[7] is the amount of worksheets we want to look at.

### Spreadsheet Walkthrough:
The spreadsheets are very simple. The first row must be done as seen below. Each comment/username can have multiple responses, and remember to fill out number of responses.

For parsing comments:
<img src="https://github.com/wlhunter00/RedditBotADP/blob/master/README%20Photos/GoogleSheetsCommentParse.JPG">

For parsing usernames:
<img src="https://github.com/wlhunter00/RedditBotADP/blob/master/README%20Photos/GoogleSheetsUserParse.JPG">

Contact William Hunter at **wlhunter00@gmail.com** with any questions or concerns.
