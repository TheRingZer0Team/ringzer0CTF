#!/usr/bin/env python3

'''

 Initial version by: jusb3 (to compare 2 users)
 Rewrote by        : TheIndian, July 4th, 2019
 Redistribution authorized by jusb3 (Who made the first comparison between two users)

 requirements: pip3 install tabulate

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

 2020-04-17v3.1:  (by TheIndian)
                  Option 5: Solve problem when user did not solve any Challange
                  Option 6: Sometime, API did not return result by date ordered. Force locally the order by date
                  Option 7: Sometime, API did not return result by date ordered. Force locally the order by date


2020-08-20v4.0b1: (by TheIndian)
                  Support the new APIs published on ~2020-06-17 on R0.
                  Option '2 Show a user information' and '3 Show a user score' merged.
                  All options reviewed, revamped, accurate with information provided by new APIs.
                  New: Show Challenges categories information.
                  New: Show Special Mentions made by a user.
                  And more...

'''

version = 'version 4.0-Beta 1'
URL  = 'https://ringzer0ctf.com'

APIURLCategories          = URL + '/api/categories'                            # Return Categories of Challenges
#APIURLCategoryInfo       = URL + '/apl/info/{categoryid}                      # Return Category informations
#APIURLCategoryChallenges = URL + '/api/category/challenges/{categoryid}       # Return Challenges in a Category
APIURLChallengeInfo       = URL + '/api/challenge/info/{challengeid}'          # Return Challenge informatons
APIURLChallengeWriteUp    = URL + '/api/challenge/writeups/{challengeid}'      # Return Write-Ups for a Challenges (limit)
APIURLUserInfo            = URL + '/api/user/info/{userid}'                    # Return a user informations
APIURLUserCategory        = URL + '/api/user/category/{userid}/{categoryid}'   # Return Challenges made by a user in a Category
#APIURLUserChallenge      = URL + '/api/user/challenge/{userid}/{challengeId}' # Return information on a Challenge made by a user
APIURLUserSpecialMention  = URL + '/api/user/specialmentions/{userid}'         # Return specials mentions made by a user
APIURLChallengeUsers      = URL + '/api/challenge/users/{challengeid}'         # Return users who solved a Challenge

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
    '\t(1)  Compare 2 users.\n'\
    '\t(2)  Show a user information and score.\n'\
    '\t(3)  Show a challenge information.\n'\
    '\t(4)  Show Challenges categories.\n'\
    '\t(5)  Show Challenges solved by a user.\n'\
    '\t(6)  Show Write-Up made by a user.\n'\
    '\t(7)  Show users who solved a challenge.\n'\
    '\t(8)  Show users who made a write up for a challenge.\n'\
    '\t(9)  Show Special Mentions made by a user.\n'\
    '\t(10) Check unsolved challenges.\n'\
    '\t(0)  Exit.\n'\
    '\n'\
    'You choice: '
    MaxMenu = 10
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
    # Option 1: Compare 2 Users
    #
    User1 = input('Enter the ID or username for user 1: ')
    User2 = input('Enter the ID or username for user 2: ')
    print ('Compare users \'{}\' vs \'{}\''.format(User1, User2))

    # Get User1 ID
    print ('  Get profile ID of \'{}\'. Please wait.'.format(User1))
    r1 = requests.get(APIURLUserInfo.format(userid=User1))
    CheckStatusCode(r1, 'Request failed user \'{}\'.'.format(User1))
    r1 = r1.json()
    if r1['success'] == 0:
        print('\nOups! User 1 \'{}\' not found. Please retry.\n'.format(User1))
        sys.exit(1)
    User1 = r1['data']['users'][0]['user']['username']
    ID1   = r1['data']['users'][0]['user']['id']

    # Get User2 ID
    print ('  Get profile ID of \'{}\'. Please wait.'.format(User2))
    r2 = requests.get(APIURLUserInfo.format(userid=User2))
    CheckStatusCode(r2, 'Request failed user \'{}\'.'.format(User2))
    r2 = r2.json()
    if r2['success'] == 0:
        print('\nOups! User 2 \'{}\' not found. Please retry.\n'.format(User2))
        sys.exit(1)
    User2 = r2['data']['users'][0]['user']['username']
    ID2   = r2['data']['users'][0]['user']['id']

    # Get Challenges completed by User1
    print ('  Get Challenges solved by \'{}\' (ID: {}). Please wait.'.format(User1, ID1))
    print ('    Profile: {}/profile/{}/{}'.format(URL, ID1, User1))
    Lst1   = []
    LstID1 = []
    for i in range(len(r1['data']['categories'])):
        if int(r1['data']['categories'][i]['category']['numberOfSolved']) != 0:
            r = requests.get(APIURLUserCategory.format(userid=User1, categoryid=r1['data']['categories'][i]['category']['id']))
            Solved = r.json()
            for j in range(len(Solved['data']['categories'][0]['category']['challenges'])):
                if Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['solved'] == True:
                    Lst1.append([int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['id']), \
                                 int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['points']), \
                                 r1['data']['categories'][i]['category']['title'], \
                                     Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['title']])
                    LstID1.append(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['id'])

    # Get Challenges completed by User2
    print ('  Get Challenges solved by \'{}\' (ID: {}). Please wait.'.format(User2, ID2))
    print ('    Profile: {}/profile/{}/{}'.format(URL, ID2, User2))
    Lst2   = []
    LstID2 = []
    for i in range(len(r2['data']['categories'])):
        if int(r2['data']['categories'][i]['category']['numberOfSolved']) != 0:
            r = requests.get(APIURLUserCategory.format(userid=User2, categoryid=r2['data']['categories'][i]['category']['id']))
            Solved = r.json()
            for j in range(len(Solved['data']['categories'][0]['category']['challenges'])):
                if Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['solved'] == True:
                    Lst2.append([int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['id']), \
                                 int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['points']), \
                                 r2['data']['categories'][i]['category']['title'], \
                                     Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['title']])
                    LstID2.append(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['id'])

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
    for i in range(len(LstID1)):
        if LstID1[i] in LstID2:
            List.append(Lst1[i])
            Points1 += Lst1[i][1]
    List = sorted(List, key = lambda x: (x[Sort1By], x[Sort2By], x[Sort3By]))   # Sort as wanted
    print (tabulate(List, headers=['ID:', 'Points:', 'Category', 'Title']))
    print ('\n{} Challenges have been solved by both \'{}\' AND by \'{}\' - ({} points)'.format(len(List), User1, User2, Points1))

    #
    # Display Challenges solved by User1 but NOT by User2
    #
    print ('\nChallenges solved by \'{}\' but NOT by \'{}\':'.format(User1, User2))
    List = []; Points2 = int()
    for i in range(len(LstID1)):
        if LstID1[i] not in LstID2:
            List.append(Lst1[i])
            Points2 += Lst1[i][1]
    List = sorted(List, key = lambda x: (x[Sort1By], x[Sort2By], x[Sort3By]))   # Sort as wanted
    print (tabulate(List, headers=['ID:', 'Points:', 'Category', 'Title']))
    print ('\n{} Challenges solved by \'{}\' but NOT by \'{}\' - ({} points)'.format(len(List), User1, User2, Points2))

    #
    # Display Challenges solved by User1 but NOT by User2
    #
    print ('\nChallenges solved by \'{}\' but NOT by \'{}\':'.format(User2, User1))
    List = []; Points3 = int()
    for i in range(len(LstID2)):
        if LstID2[i] not in LstID1:
            List.append(Lst2[i])
            Points3 += Lst2[i][1]
    List = sorted(List, key = lambda x: (x[Sort1By], x[Sort2By], x[Sort3By]))   # Sort as wanted
    print (tabulate(List, headers=['ID:', 'Points:', 'Category', 'Title']))
    print ('\n{} Challenges solved by \'{}\' but NOT by \'{}\' - ({} points)\n'.format(len(List), User2, User1, Points3))
    print ('The user \'{}\' has {} points.  '.format(User1, Points1 + Points2))
    print ('The user \'{}\' has {} points.\n'.format(User2, Points1 + Points3))


def ShowUserInfo():
    #
    # Option 2: Show a user information and score.
    #
    MsgGetUser = 'Enter the ID or username: '
    User = input(MsgGetUser)
    r = requests.get(APIURLUserInfo.format(userid=User))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(User))
    user = r.json()
    Solved = 0; NbrChals = 0;
    if user['success'] == 1: 
        print('\nID:               {}'.format(user['data']['users'][0]['user']['id']))
        print('Username:         {}'.format(user['data']['users'][0]['user']['username']))
        print('Country:          {}'.format(user['data']['users'][0]['user']['country']))
        print('Member since:     {}'.format(user['data']['users'][0]['user']['memberSince']))
        print('Profile:          {}/profile/{}/{}'.format(URL, user['data']['users'][0]['user']['id'], user['data']['users'][0]['user']['username']))
        print('Points:           {} / {}'.format(user['data']['users'][0]['user']['points'], user['data']['users'][0]['user']['maxpoints']))
        print('Rank:             {} / {} of users.'.format(user['data']['users'][0]['user']['rank']  , user['data']['users'][0]['user']['totalPlayers']))
        print('Coins:            {}'.format(user['data']['users'][0]['user']['coins']))
        print('RCEH:             {}'.format(user['data']['users'][0]['user']['isRCEH']))
        print('Special Mentions: {}'.format(user['data']['users'][0]['user']['specialmentions']))
        print('Last submit:      {}'.format(user['data']['users'][0]['user']['lastFlag']))
        print('Challenges completed:\n')
        List = []
        for i in range(len(user['data']['categories'])):
            Solved += int(user['data']['categories'][i]['category']['numberOfSolved'])
            NbrChals += int(user['data']['categories'][i]['category']['numberOfChallenges'])

            List.append(['', user['data']['categories'][i]['category']['title'], \
                             user['data']['categories'][i]['category']['numberOfSolved'] + ' / ' + \
                             user['data']['categories'][i]['category']['numberOfChallenges']])
        List = sorted(List, key = lambda x: (x[1]))
        List.append(['','------------------------', '---------'])
        List.append(['', 'Total Challenges solved:', str(Solved) + ' / ' + str(NbrChals)])
        print (tabulate(List, headers=['', 'Title:', 'Completed']))
        print ('\n')
    else:
        raise Exception ('\nOups! ID or username \'{}\' not found. Please retry.\n'.format(User))


def ShowChallengeInfo():
    #
    # Option 3: Show a challenge information.
    #
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = GetANumber(MsgGetChallengeID)
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
    challenge = r.json()
    if challenge['success'] == 1:
        print('\nID:              {}'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['id']))
        print('Title:           {}'.format( challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['title']))
        print('Category:        {} (category id {})'.format(challenge['data']['categories'][0]['category']['title'], \
                                                            challenge['data']['categories'][0]['category']['id']))
        print('Points:          {}'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['points']))
        print('Published:       {}'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['publishDate']))
        print('Author:          {}'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['author']))
        print('Solved:          {}'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['numberOfSolves']))
        print('Write-up:        {}'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['numberOfWriteUps']))
        print('Last solved by:  {} on {}\n'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['lastSubmitUserName'], \
                                                   challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['lastSubmitDate']))
    else:
        raise Exception ('\nOups! Challenge \'{}\' doesn\'t exist.\n'.format(ChallengeID))


def ShowCategories():
    #
    # Option 4: Show Challenges Categories
    #
    print ('\n')
    r = requests.get(APIURLCategories)
    CheckStatusCode(r, 'Request failed.')
    categories = r.json()
    List = []
    if categories['success'] == 1:
        for i in range(len(categories['data']['categories'])):
            List.append([categories['data']['categories'][i]['category']['title'], \
                         categories['data']['categories'][i]['category']['id'], \
                         categories['data']['categories'][i]['category']['numberOfChallenges']])
    List = sorted(List, key = lambda x: (x[0], x[1], x[2]))
    print (tabulate(List, headers=['Title:', 'ID:', '#Chal:']))
    print ('\nNumber of categories: {}'.format(len(categories['data']['categories'])))


def ShowChallengesSolvedByUser():
    #
    # Option 5: Show Challenges solved by a user
    #
    MsgGetUser = 'Enter the ID or username: '
    Username = input(MsgGetUser)
    r = requests.get(APIURLUserInfo.format(userid=Username))
    CheckStatusCode(r, 'Request failed to get user \'{}\''.format(Username))
    User = r.json()
    if User['success'] == 1:
        Username = User['data']['users'][0]['user']['username']
        ID   =     User['data']['users'][0]['user']['id']
        print ('  Get Challenges solved by \'{}\' (ID: {}). Please wait.'.format(Username, ID))
        print ('    Profile: {}/profile/{}/{}\n'.format(URL, ID, Username))
        Message = 'How would you like to sort by?\n 0 = date (defaut), 1 = category, 2 = Challange name, 3 = Points, 4 = ID\nYou choice: '
        true = True
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
        print('Retrieving Challenges solved by \'{}\'. Please wait...'.format(Username))
        List   = []; Points = int()
        NbrChal, NbrSolved = 0, 0
        for i in range(len(User['data']['categories'])):
            NbrChal += int( User['data']['categories'][i]['category']['numberOfChallenges'])
            if int(User['data']['categories'][i]['category']['numberOfSolved']) != 0:
                r = requests.get(APIURLUserCategory.format(userid=Username, categoryid=User['data']['categories'][i]['category']['id']))
                Solved = r.json()
                for j in range(len(Solved['data']['categories'][0]['category']['challenges'])):
                    if Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['solved'] == True:
                        NbrSolved += 1
                        List.append([Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['validationTime'],\
                                 User['data']['categories'][i]['category']['title'], \
                                 Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['title'], \
                                 int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['points']), \
                                 int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['id']) ])
                        Points += int(Solved['data']['categories'][0]['category']['challenges'][j]['challenge']['points'])
        List = sorted(List, key = lambda x: (x[entry]))
        print ('\n', tabulate(List, headers=['Date:', 'Category:', 'Title:', 'Points:', 'ID:']))
        print ('\n The total points for \'{}\' is {} in {} Challenges solved on {}.\n'.format(Username, Points, NbrSolved, NbrChal))
    else:
        raise Exception ('\nOups! ID or username \'{}\' not found. Please retry.\n'.format(Username))


def ShowWriteUpByUser():
    #
    # Option 6: Show Write-Up made by a user
    #
    MsgGetUser = 'Enter the ID or username: '

    print ('\n\nThis option is not available for this moment. It will be in the next version.\n\n')


def ShowWhoSolvedChallenge():
    #
    # Option 7: Show users who solved a challenge.
    #
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = GetANumber(MsgGetChallengeID)
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
    challenge = r.json()
    if(challenge['success'] == 1):
        Limit = input('How many last users who solved the Challange would you like to retrieve (enter for all) ? ')
        if len(Limit) > 0:
            Limit = '/' + str(Limit)
        else:
            Limit = ''
        print('\nChallange name: {} / {} / {} points.'.format(\
                challenge['data']['categories'][0]['category']['title'],
                challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['title'],
                challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['points'] ))
        r = requests.get((APIURLChallengeUsers+Limit).format(challengeid=ChallengeID))
        CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
        print ('\nSolved by:\n')
        Users = r.json()
        List = []
        for i in range(len(Users['data']['categories'][0]['category']['challenges'][0]['challenge']['Solvers'])):
            List.append([Users['data']['categories'][0]['category']['challenges'][0]['challenge']['Solvers'][i]['Solver']['validationTime'], \
                         Users['data']['users'][i]['user']['username']])
        List = (sorted(List))
        Submit = []
        for i in range(len(List)):
            Submit.append([i+1, List[i][0],  List[i][1]])
        print (tabulate(Submit, headers=['Rank:', 'Submitted:', 'Users:']))
        if Limit == '':
            print('\nNumber of solves: {}\n'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['numberOfSolves']))
        else:
            print('\nNumber of solves {}, but retrieved only the last {}.\n'.format(\
                    challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['numberOfSolves'], \
                    len(Users['data']['categories'][0]['category']['challenges'][0]['challenge']['Solvers'])))
    else:
        raise Exception ('\nOups! Challenge \'{}\' doesn\'t exist.\n'.format(ChallengeID))


def ShowWriteUp():
    #
    # Option 8: Show users who made a write up for a challenge.
    #
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = GetANumber(MsgGetChallengeID)
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
    challenge = r.json()
    if(challenge['success'] == 1):
        Limit = input('How many write-ups would you like to retrieve. All S.M. are shown (enter for all) ? ')
        if len(Limit) > 0:
            Limit = '/' + str(Limit)
        else:
            Limit = ''
        print('\nChallange name: {} / {} / {} points.'.format(challenge['data']['categories'][0]['category']['title'], \
                                                              challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['title'], \
                                                              challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['points']))
        r = requests.get((APIURLChallengeWriteUp+Limit).format(challengeid=ChallengeID))
        CheckStatusCode(r, 'Request failed to get Challange \'{}\''.format(ChallengeID))
        Users = r.json()
        List = []
        for i in range(len(Users['data']['users'])):
            if Users['data']['categories'][0]['category']['challenges'][0]['challenge']['writeUps'][i]['writeUp']['isSpecialMention'] == True:
                List.append([Users['data']['categories'][0]['category']['challenges'][0]['challenge']['writeUps'][i]['writeUp']['receivedTime'], \
                             Users['data']['categories'][0]['category']['challenges'][0]['challenge']['writeUps'][i]['writeUp']['id'], \
                             Users['data']['users'][i]['user']['username'], \
                             'Special Mention' ])
            else:
                List.append([Users['data']['categories'][0]['category']['challenges'][0]['challenge']['writeUps'][i]['writeUp']['receivedTime'], \
                             Users['data']['categories'][0]['category']['challenges'][0]['challenge']['writeUps'][i]['writeUp']['id'], \
                             Users['data']['users'][i]['user']['username'], \
                             '' ])
        List = (sorted(List))
        WriteUp = []
        for i in range(len(List)):
            WriteUp.append([i+1, List[i][0],  List[i][1],  List[i][2], List[i][3]])
        print ('\n', tabulate(WriteUp, headers=['Rank:', 'Submitted:', 'Doc ID:', 'Username', 'Special Mention:']))
        if Limit == '':
            print('\nNumber of write up: {}\n'.format(challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['numberOfWriteUps']))
        else:
            print('\nNumber of write up {}, but retrieved only the last {} (priorizing the Specials Mentions).\n'.format(\
                    challenge['data']['categories'][0]['category']['challenges'][0]['challenge']['numberOfWriteUps'], \
                    len(Users['data']['users'])))
    else:
        raise Exception('\nOups! Challenge \'{}\' does not exist.\n'.format(ChallengeID))


def ShowSpecialMentionByUser():
    #
    # Option 9: Show Special Mention made by a user
    #
    User = input('Enter the ID or username: ')
    print ('  Get profile ID of \'{}\'. Please wait.'.format(User))
    r = requests.get(APIURLUserSpecialMention.format(userid=User))
    CheckStatusCode(r, 'Request failed user \'{}\'.'.format(User))
    sm = r.json()
    if sm['success'] == 1:
        Username = sm['data']['users'][0]['user']['username']
        ID = sm['data']['users'][0]['user']['id']
        print('\nFollowing are the Spacial Mention received by \'{}\' (ID: {})'.format(Username, ID))
        List = []
        for i in range(len(sm['data']['categories'])):
            for j in range(len(sm['data']['categories'][i]['category']['challenges'])):
                List.append([sm['data']['categories'][i]['category']['challenges'][j]['challenge']['writeUps'][0]['writeUp']['receivedTime'], \
                             sm['data']['categories'][i]['category']['title'], \
                             sm['data']['categories'][i]['category']['challenges'][j]['challenge']['id'], \
                             sm['data']['categories'][i]['category']['challenges'][j]['challenge']['title'], \
                             sm['data']['categories'][i]['category']['challenges'][j]['challenge']['writeUps'][0]['writeUp']['id'] ])
        WriteUp = sorted(List, key = lambda x: (x[0], x[1], x[3], x[4]))   # Sort as wanted
        print ('\n', tabulate(WriteUp, headers=['Submitted:', 'Category', 'ChalID:', 'Title', 'DocID:']))
        print('\nNumber of write up: {}\n'.format(len(List)))

    else:
        raise Exception ('\nOups! ID or username \'{}\' not found. Please retry.\n'.format(User))


def UnsolvedRing0():
    #
    # Option 10: Check unsolved Challanges
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
            raise Exception('\nOups! This script is executable on Python3 only!\n')
        PrintBanner()
        Choice = MainMenu()
        if(Choice == 1):
            CompareTwoUsers()
        if(Choice == 2):
            ShowUserInfo()
        if(Choice == 3):
            ShowChallengeInfo()
        if(Choice == 4):
            ShowCategories()
        if(Choice == 5):
            ShowChallengesSolvedByUser()
        if(Choice == 6):
            ShowWriteUpByUser()
        if(Choice == 7):
            ShowWhoSolvedChallenge()
        if(Choice == 8):
            ShowWriteUp()
        if(Choice == 9):
            ShowSpecialMentionByUser()
        if(Choice == 10):
            UnsolvedRing0()
        if(Choice == 0):
            raise Exception('Thank for using this script')
    except Exception as e:
        print(e)
        sys.exit(1)

