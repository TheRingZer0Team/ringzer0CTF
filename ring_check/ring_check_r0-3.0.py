#!/usr/bin/env python3

'''

 Initial version by: jusb3
 Rewrote by        : TheIndian, July 4th, 2019
 Redistribution authorized by jusb3 (Who made the first comparison between two users)
 New features:
     - Work with Python3 only
     - Display the same Challenges solved by User1 AND User2
     - Display the Challenges solved by User1 but NOT by User2
     - Display the Challenges solved by User2 but NOT by User1
     - Challenges displayed with names instead of with the number

 2019-07-08 :     Search improved and accurate
                  Display improved

 2019-07-08v2.1:  Use API to retrieve profile ID
                  Display improved
 2019-07-08v2.2:  Username case insensitive
 2019-10-07v2.3:  Fixed typos (by mbergeron)
 2019-10-07v2.4:  Added some new features according to the API (by mbergeron)
 2019-11-13v2.5:  (by theindian)
                  Option 1: Display user ID and user Profile link
                  Option 2: Display user Profile link
                  Option 3: Could enter user ID or username
                  Option 3: Display the username
                  Option 3: Display user Profile link
 2019-12-14v2.6:  Add option 6: List users who made a write up for a challenge (by TheIndian)
 2019-12-15v2.7:  (by TheIndian)
                  Cosmetic 
                  Option 5: Display the Challenge category / Challenge name
                  Option 6: Sort the output list
 2020-03-07v3.0:  (by TheIndian)
                  A special thank to @mbergeron for his help to modify on RZ the APIs output for new requirements
                  A spaciel thank to @davidlebr1 for his help for sanitizing check
                  Menu sanitized and more interactive
                  Option 1: Completly rewroted. APIs fully supported
                            NEW: Output may be sorted as wanted. See Sort1By, Sort2By and Sort3By variables
                  Option 2: Input and output sanitized
                            NEW: Show Member since
                  Option 3: Input and output sanitized
                            NEW: Show the Number of Special Mention
                            Partially solved the inaccuracy information provided by the API
                  Option 4: Input and output sanitized
                  Option 5: NEW option: Show Challanges solved by a user
                  Option 6: NEW: Show solved date and sort by date
                                 Show rank of solved
                  Option 7: NEW: write-up date submitted and sort by date
                                 Show rank of solved
                  Option 8: NEW: Execute unsolved_r0.py
                  Make sure the script is executed in Python3
                  New name
                  Cosmetic

'''

version = 'version 3.0'
URL  = 'https://ringzer0ctf.com'
APIURLUserInfo = URL + '/api/user/{user}'
APIURLUserScore = URL + '/api/score/{userid}'
APIURLChallengeInfo = URL + '/api/challenge/{challengeid}'
APIURLListUserByChallenge = URL + '/api/solved/{challengeid}'
APIURLListWhoMadeWriteUp = URL + '/api/writeup/{challengeid}'

import json
import re, sys, os, platform
import requests
from tabulate import tabulate

def PrintBanner():
    print('   ___  _          ____          ___')
    print('  / _ \\(_)__  ___ /_  / ___ ____/ _ \\')
    print(' / , _/ / _ \\/ _ `// /_/ -_) __/ // /')
    print('/_/|_/_/_//_/\\_, //___/\\__/_/  \\___/')
    print('            /___/ {}\n'.format(version))


def MainMenu():
    MsgOptionMenu = \
    'Choose an option between:\n'\
    '\t(1)  Compare 2 users\n'\
    '\t(2)  Show a user information\n'\
    '\t(3)  Show a user score\n'\
    '\t(4)  Show a challenge information\n'\
    '\t(5)  Show Challenges solved by a user\n'\
    '\t(6)  Show users who solved a challenge\n'\
    '\t(7)  Show users who made a write up for a challenge\n'\
    '\t(8)  Check unsolved challenges\n'\
    '\t(0)  Exit\n'\
    '\n'\
    'You choice: '
    MaxMenu = 8
    while True:
        try:
            entry = int(input(MsgOptionMenu))
            if entry >= 0 and entry <= MaxMenu:
                return entry
            else:
                print (' *** Invalid number. Please retry ***')
        except:
            print (' *** Invalid input. Please retry ***')


def CheckStatusCode(Status, Message):
    if Status.status_code != 200:
        raise Exception('\n  {}:\t{}\n'.format(Message, Status))


def GetANumber(Message):
    while True:
        entry = input(Message)
        try:
            entry = int(entry)
            return entry
        except:
            print (' *** Invalid number. Please retry ***')


def CompareTwoUsers():
    #
    # Compare two Users
    #
    User1 = input('Enter the ID or username for user 1: ')
    User2 = input('Enter the ID or username for user 2: ')
    print ('Compare users \'{}\' vs \'{}\''.format(User1, User2))

    # Get User1 information's
    print ('  Get profile ID of \'{}\'. Please wait.'.format(User1))
    r = requests.get(APIURLUserInfo.format(user=User1))
    CheckStatusCode(r, 'Request failed user \'{}\'.'.format(User1))
    r = r.json()
    if r['success'] == 0:
        print('\nOups! User 1 \'{}\' not found. Please retry.\n'.format(User1))
        sys.exit(1)
    User1 = r['user'][0]['username']
    ID1   = r['user'][0]['id']
    print ('  Get Challenges solved by \'{}\' (ID: {}). Please wait.'.format(User1, ID1))
    print ('    Profile: {}/profile/{}/{}'.format(URL, ID1, User1))
    r = requests.get(APIURLUserScore.format(userid=User1))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(User1))
    Lst1 = r.json()
    Lst1ID = []
    for Category in enumerate(Lst1['challenges']):
        for j in enumerate(Lst1['challenges'][Category[1]]):
            Lst1ID.append(j[1]['id'])

    # Get User2 information's
    print ('  Get profile ID of \'{}\'. Please wait.'.format(User2))
    r = requests.get(APIURLUserInfo.format(user=User2))
    CheckStatusCode(r, 'Request failed user \'{}\'.'.format(User2))
    r = r.json()
    if r['success'] == 0:
        print('\nOups! User 2 \'{}\' not found. Please retry.\n'.format(User2))
        sys.exit(1)
    User2 = r['user'][0]['username']
    ID2   = r['user'][0]['id']
    print ('  Get Challenges solved by \'{}\' (ID: {}). Please wait.'.format(User2, ID2))
    print ('    Profile: {}/profile/{}/{}'.format(URL, ID2, User2))
    r = requests.get(APIURLUserScore.format(userid=User2))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(User2))
    Lst2 = r.json()
    Lst2ID = []
    for Category in enumerate(Lst2['challenges']):
        for j in enumerate(Lst2['challenges'][Category[1]]):
            Lst2ID.append(j[1]['id'])

    # Sort1by = First sort by...
    # Sort2By = Second sort by...
    # Sort3By = Third sort by...
    #      0 = Sort by ID;
    #      1 = Sort by Points;
    #      2 = Sort by Category;
    #      3 = Sort by Challenge Name;
    # Ex: Sort1By = 2; Sort2By = 1; Sort3By = 3 # 1st sort by Category, 2nd sort by Points, 3rd sort by Chal Name
    Sort1By = 2; Sort2By = 1; Sort3By = 3

    #
    # Display Same Challenges solved by User1 AND by User2
    #
    print ('\nSame Challenges solved by \'{}\' AND by \'{}\':'.format(User1, User2))
    List = []; Points1 = int()
    for Category in enumerate(Lst1['challenges']):
        for j in enumerate(Lst1['challenges'][Category[1]]):
            if j[1]['id'] in Lst2ID:
                List.append([int(j[1]['id']), int(j[1]['points']), Category[1], j[1]['title']])
                Points1 += int(j[1]['points'])
    List = sorted(List, key = lambda x: (x[Sort1By], x[Sort2By], x[Sort3By]))   # Sort as wanted
    print (tabulate(List, headers=['ID:', 'Points:', 'Category', 'Title']))
    print ('\n{} Challenges have been solved by both \'{}\' AND by \'{}\' - ({} points)'.format(len(List), User1, User2, Points1))


    #
    # Display Challenges solved by User1 but NOT by User2
    #
    print ('\nChallenges solved by \'{}\' but NOT by \'{}\':'.format(User1, User2))
    List = []; Points2 = int()
    for Category in enumerate(Lst1['challenges']):
        for j in enumerate(Lst1['challenges'][Category[1]]):
            if j[1]['id'] not in Lst2ID:
                List.append([int(j[1]['id']), int(j[1]['points']), Category[1], j[1]['title']])
                Points2 += int(j[1]['points'])
    List = sorted(List, key = lambda x: (x[Sort1By], x[Sort2By], x[Sort3By]))   # Sort as wanted
    print (tabulate(List, headers=['ID:', 'Points:', 'Category', 'Title']))
    print ('\n{} Challenges solved by \'{}\' but NOT by \'{}\' - ({} points)'.format(len(List), User1, User2, Points2))


    #
    # Display Challenges solved by User1 but NOT by User2
    #
    print ('\nChallenges solved by \'{}\' but NOT by \'{}\':'.format(User2, User1))
    List = []; Points3 = int()
    for Category in enumerate(Lst2['challenges']):
        for j in enumerate(Lst2['challenges'][Category[1]]):
            if j[1]['id'] not in Lst1ID:
                List.append([int(j[1]['id']), int(j[1]['points']), Category[1], j[1]['title']])
                Points3 += int(j[1]['points'])
    List = sorted(List, key = lambda x: (x[Sort1By], x[Sort2By], x[Sort3By]))   # Sort as wanted
    print (tabulate(List, headers=['ID:', 'Points:', 'Category', 'Title']))
    print ('\n{} Challenges solved by \'{}\' but NOT by \'{}\' - ({} points)\n'.format(len(List), User2, User1, Points3))
    print ('The user \'{}\' has {} points.  '.format(User1, Points1 + Points2))
    print ('The user \'{}\' has {} points.\n'.format(User2, Points1 + Points3))


def ShowUserInfo():
    #
    # Show a User informations'
    #
    MsgGetUser = 'Enter the ID or username: '
    User = input(MsgGetUser)
    r = requests.get(APIURLUserInfo.format(user=User))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(User))
    user = r.json()
    if len(user['user']) > 0:
        print('\nID:           {}'.format(user['user'][0]['id']))
        print('User:         {}'.format(user['user'][0]['username']))
        print('Member since: {}'.format(user['user'][0]['member_since']))
        print('Profile:      {}/profile/{}/{}\n'.format(URL, user['user'][0]['id'], user['user'][0]['username']))
    else:
        raise Exception ('\nOups! ID or username \'{}\' not found. Please retry.\n'.format(User))


def ShowUserScore():
    #
    # Show a user score information's
    #
    MsgGetUser = 'Enter the ID or username: '
    User = input(MsgGetUser)
    r = requests.get(APIURLUserInfo.format(user=User))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(User))
    UserID = r.json()
    if UserID['success'] == 1:
        Username = UserID['user'][0]['username']
        UserID   = UserID['user'][0]['id']
        r = requests.get(APIURLUserScore.format(userid=Username))
        CheckStatusCode(r, 'Request failed to get user \'{}\''.format(Username))
        user = r.json()
        # print('\nWARNING: This API call has some issues and therefore, the data could be false.')
        print('\nUsername: {}'.format(Username))
        print('ID:       {id}'.format(id = user['user']))
        print('Score:    {score}/{maxScore}'.format(score=user['score'], maxScore=user['maxscore']))
        print('Rank:     {rank}/{totalPlayers}'.format(rank=user['rank'], totalPlayers=user['totalplayers']))
        print('S.M.:     {sm} Special Mention'.format(sm = user['specialmentions']))
        if  user['solved'] != 0:
            print('Solved:   {solved}/{totalChallenges}'.format(solved=user['solved'], totalChallenges=user['totalchallenges']))
        else:
            print('Solved:   {solved}'.format(solved=user['solved']))
        print('Profile:  {}/profile/{}/{}\n'.format(URL, user['user'], Username))
    else:
        raise Exception ('\nOups! ID or username \'{}\' not found. Please retry.\n'.format(User))


def ShowChallengeInfo():
    #
    # Show a Challenge information's
    #
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = GetANumber(MsgGetChallengeID)
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
    challenge = r.json()
    if len(challenge) > 1:
        print('\nID:          {}'.format(challenge['challenge']['id']))
        print('Title:       {}'.format(challenge['challenge']['title']))
        print('Category:    {}'.format(challenge['challenge']['category']))
        print('Points:      {}'.format(challenge['challenge']['points']))
        print('Author:      {}'.format(challenge['challenge']['author']))
        print('Last Submit: {}'.format(challenge['challenge']['lastSubmit']))
        print('Validated:   {}\n'.format(challenge['challenge']['validated']))
    else:
        raise Exception ('\nOups! Challenge \'{}\' doesn\'t exist.\n'.format(ChallengeID))


def ShowChallengesSolvedByUser():
    #
    # Show Challenges solved by a user
    #
    MsgGetUser = 'Enter the ID or username: '
    User = input(MsgGetUser)
    r = requests.get(APIURLUserInfo.format(user=User))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(User))
    UserID = r.json()
    if UserID['success'] == 1:
        Username = UserID['user'][0]['username']
        UserID   = UserID['user'][0]['id']
        print ('  Get Challenges solved by \'{}\' (ID: {}). Please wait.'.format(Username, UserID))
        print ('    Profile: {}/profile/{}/{}\n'.format(URL, UserID, Username))
        Message = 'How would you like to sort by?\n 0 = date (defaut), 1 = category, 2 = Challange name, 3 = Points, 4 = ID\nYou choice: '
        true = True ; 
        while true:
            entry = input(Message)
            try:
                entry = int(entry)
                if 0 <= entry and entry <= 4:
                    break
                else:
                    print (' *** Invalid number. Please retry ***')
            except:
                if entry == '':
                    entry = 0       # Default, sort by date
                    true = False
                else:
                    print (' *** Invalid number. Please retry ***')
        r = requests.get(APIURLUserScore.format(userid=Username))
        CheckStatusCode(r, 'Request failed to get user \'{}\''.format(Username))
        Solved = r.json()
        List = []; Points = int()
        for Category in enumerate(Solved['challenges']):
            for j in enumerate(Solved['challenges'][Category[1]]):
                List.append([j[1]['date'], Category[1], j[1]['title'], int(j[1]['points']), int(j[1]['id'])])
                Points += int(j[1]['points'])
        List = sorted(List, key = lambda x: (x[entry])) # Sort by, see upstair!
        print (tabulate(List, headers=['Date:', 'Category:', 'Title:', 'Points:', 'ID:']))
        print ('\n Total points for \'{}\' is {}. {} Challenges solved on {}.\n'.format(Username, Points,Solved['solved'], Solved['totalchallenges']))
    else:
        raise Exception ('\nOups! ID or username \'{}\' not found. Please retry.\n'.format(User))


def ShowUsersByChallenge():
    #
    # Show Users that solved a Challenge
    #
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = GetANumber(MsgGetChallengeID)
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
    challenge = r.json()
    if(challenge['success'] == 1):
        print('\nChallange name: {} / {} / {} points.'.format(challenge['challenge']['category'], challenge['challenge']['title'], challenge['challenge']['points']))
        r = requests.get(APIURLListUserByChallenge.format(challengeid=ChallengeID))
        CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
        print ('Solved by:\n')        #\t  {}\t{}'.format('Date of solved:', 'Users:'))
        Users = r.json()
        List = []
        Let = 1
        for i in Users['solved']:
            List.append([Let, i[1], i[0]])
            Let += 1
        print (tabulate(List, headers=['Rank:', 'Submitted:', 'Users:']))
        print('\nNumber of solves: {}\n'.format(len(Users['solved'])))
    else:
        raise Exception ('\nOups! Challenge \'{}\' doesn\'t exist.\n'.format(ChallengeID))


def ShowWriteUpByChallenge():
    #
    # Show Users that submitted a write-up
    #
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = GetANumber(MsgGetChallengeID)
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
    challenge = r.json()
    if(challenge['success'] == 1):
        print('\nChallange name: {} / {} / {} points.'.format(challenge['challenge']['category'], challenge['challenge']['title'], challenge['challenge']['points']))
        r = requests.get(APIURLListWhoMadeWriteUp.format(challengeid=ChallengeID))
        CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
        Users = r.json()
        print('Write up made by:\n')
        WriteUp = []
        Let = 1
        for User in range(len(Users['writeup'])):
            if(int(Users['writeup'][User]['specialmention']) == 1):
                WriteUp.append([Let, Users['writeup'][User]['receivedtime'], Users['writeup'][User]['user'],'Special mention'])
            else:
                WriteUp.append([Let, Users['writeup'][User]['receivedtime'], Users['writeup'][User]['user'],''])
            Let += 1
        WriteUp = (sorted(WriteUp))
        print (tabulate(WriteUp, headers=['Rank:', 'Submitted:', 'Users:', 'Special Mention:']))
        print('\nNumber of write up: {}\n'.format(len(Users['writeup'])))
    else:
        raise Exception('\nOups! Challenge \'{}\' does not exist.\n'.format(ChallengeID))


def UnsolvedRing0():
    #
    # Check unsolved Challanges
    #
    # Because I did not receive the authaurisation from the owner to put the codei
    # here, I just call the 'unsolved_ro.py'
    #
    Unsolver = './unsolved_r0.py'
    if not os.path.isfile(Unsolver):
        print ('\nOups! The script \'{}\' does not exist!'.format(Unsolver))
        print ('\n Make sure to have the latest \'{}\' script locally. Could be found at:'.format(Unsolver))
        print ('   New version:   https://github.com/theindianCTF/R0Unsolved')
        print ('   Original from: https://github.com/JesseEmond/R0Unsolved')
        raise Exception ('\nPlease verify.\n')
    MsgGetUser = '\nEnter the ID or username: '
    User = input(MsgGetUser)
    os.system('{} {}'.format(Unsolver, User) )
    print ('\n')


if __name__=='__main__':
    os.system("stty erase '^h'")
    try:
        if platform.python_version()[0:2] != '3.':
            raise Exception('\nOups! Script must be executed on Python3.\n')
        PrintBanner()
        Choice = MainMenu()
        if(Choice == 1):
            CompareTwoUsers()
        if(Choice == 2):
            ShowUserInfo()
        if(Choice == 3):
            ShowUserScore()
        if(Choice == 4):
            ShowChallengeInfo()
        if(Choice == 5):
            ShowChallengesSolvedByUser()
        if(Choice == 6):
            ShowUsersByChallenge()
        if(Choice == 7):
            ShowWriteUpByChallenge()
        if(Choice == 8):
            UnsolvedRing0()
        if(Choice == 0):
            raise Exception('Thank for using this script')
    except Exception as e:
        print(e)
        sys.exit(1)

