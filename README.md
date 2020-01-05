# RedditBotADP
## Introduction
This is a reddit bot that I created that will parse through all of the comments in a subreddit, and reply to them based on certain keywords or certain users that did the commenting. The list of users and words to look for are stored within a Google Sheets document.
This bot can be scaled to look for many different things in the comment, such as comment score, and the type of reply can also be scaled to be more complex.

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
* [Walkthroughs](#Walkthroughs)
  * [Functions Walkthrough](#functions-walkthrough)
  * [Text file Walkthrough](#textfile-walkthrough)
  * [Spreadsheet Walkthrough](#spreadsheet-walkthrough)
* [Technologies](#technologies)
* [Installation](#installation)
* [Typical Errors](#typical-errors)

## Project Status
###### **Version 1.2**

Stable build is currently ready.

###### **Recently Added**
- [X] Created this README as a guide to the application.
- [X] Allowed for users to be parsed

#### To Do:
- [ ] Allow the responses from the bot to interact with the comment.
- [ ] Create "Smart" responses that can answer questions/
