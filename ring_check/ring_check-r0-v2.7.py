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

 2019-07-08 : Search improved and accurate
              Display improved

 2019-07-08v2.1: Use API to retrieve profile ID
                 Display improved
 2019-07-08v2.2: Username case insensitive
 2019-10-07v2.3: Fixed typos (by mbergeron)
 2019-10-07v2.4: Added some new features according to the API (by mbergeron)
 2019-11-13v2.5: (by theindian)
                 Option 1: Display user ID and user Profile link
                 Option 2: Display user Profile link
                 Option 3: Could enter user ID or username
                 Option 3: Display the username
                 Option 3: Display user Profile link
 2019-12-14v2.6: Add option 6: List users who made a write up for a challenge (by TheIndian)
 2019-12-15v2.7: (by TheIndian)
                 Cosmetic 
                 Option 5: Display the Challenge category / Challenge name
                 Option 6: Sort the output list

'''

import json
import re, sys
import requests
import urllib.request as urllib

URL  = 'https://ringzer0ctf.com'
APIURLUserInfo = URL + '/api/user/{user}'
APIURLUserScore = URL + '/api/score/{userid}'
APIURLChallengeInfo = URL + '/api/challenge/{challengeid}'
APIURLListUserByChallenge = URL + '/api/solved/{challengeid}'
APIURLListWhoMadeWriteUp = URL + '/api/writeup/{challengeid}'

def PrintBanner():
    print("   ___  _          ____          ___ \n")
    print("  / _ \\(_)__  ___ /_  / ___ ____/ _ \\\n")
    print(" / , _/ / _ \\/ _ `// /_/ -_) __/ // /\n")
    print("/_/|_/_/_//_/\\_, //___/\\__/_/  \\___/ \n")
    print("            /___/                    \n")

def MainMenu():
    MsgOptionMenu = \
    'Choose an option between:\n'\
    '\t(1) Compare 2 users\n'\
    '\t(2) Show a user information\n'\
    '\t(3) Show a user score\n'\
    '\t(4) Show a challenge information\n'\
    '\t(5) List users who solved a challenge\n'\
    '\t(6) List users who made a write up for a challenge\n'\
    '\t(0) Exit\n'\
    '\n'\
    'You choice: '
    return int(input(MsgOptionMenu))

def CompareTwoUsers():
    MsgGetUser1 = 'Enter the name of user 1: '
    MsgGetUser2 = 'Enter the name of user 2: '
    
    User1 = input(MsgGetUser1)
    User2 = input(MsgGetUser2)

    print ('Compare users ' + User1 + ' vs ' + User2)

    print (' Get profile ID of ' + User1 + '. Please wait.')
    Tmp = str(urllib.urlopen(URL+"/api/user/"+User1).read())
    if Tmp.lower().find(str(User1).lower()) == -1:
        print('\nOups! User 1 ' + User1 + ' not found!')
        sys.exit(1)
    User1 = Tmp[Tmp.find("username\":\"")+11:Tmp.find("\"}]}")]
    ID1 = Tmp[Tmp.find("\"id\":\"")+6:Tmp.find("\",\"username")]
    User1 = (Tmp[Tmp.find("\"username\":\"")+12:Tmp.find("\"}]}")])

    print (' Get profile ID of ' + User2 + '. Please wait.')
    Tmp = str(urllib.urlopen(URL+"/api/user/"+User2).read())
    if Tmp.lower().find(str(User2).lower()) == -1:
        print('\nOups! User 2 ' + User2 + ' not found!')
        sys.exit(1)
    User2 = Tmp[Tmp.find("username\":\"")+11:Tmp.find("\"}]}")]
    ID2 = Tmp[Tmp.find("\"id\":\"")+6:Tmp.find("\",\"username")]
    User2 = (Tmp[Tmp.find("\"username\":\"")+12:Tmp.find("\"}]}")])

    print (' Get Challenges solved by ' + User1 + ' (ID:' + ID1 + ') Please wait.')
    print ('    Profile: ' + URL+'/profile/'+ID1+'/'+User1)
    Tmp = urllib.urlopen(URL+'/profile/'+ID1).read()
    Lst1 = re.findall(b'><div style="width: 150px; display: inline-block"><b>(\S*.*)',Tmp); Lst1.sort()
    for i in range(len(Lst1)):
        Lst1[i] = str(Lst1[i]).replace("</a>'","").replace("</a>\"","").replace("</b></div>"," / ").replace("b'","").replace("b\"","")

    print (' Get Challenges solved by ' + User2 + ' (ID:' + ID2 + ') Please wait.')
    print ('    Profile: ' + URL+'/profile/'+ID2+'/'+User2)
    Tmp = urllib.urlopen(URL+'/profile/'+ID2).read()
    Lst2 = re.findall(b'><div style="width: 150px; display: inline-block"><b>(\S*.*)',Tmp); Lst2.sort()
    for i in range(len(Lst2)):
        Lst2[i] = str(Lst2[i]).replace("</a>'","").replace("</a>\"","").replace("</b></div>"," / ").replace("b'","").replace("b\"","")

    print ('\nSame Challenges solved by ' + User1 + ' AND by ' + User2 + ':')
    C = 0
    for k in range(len(Lst2)):
        if Lst2[k] in Lst1:
             C += 1
             print ('\t' + str(Lst2[k]))
    print (str(C) + ' Challenges have been solved by both ' + User1 + ' AND by ' + User2)

    print ('\nChallenges solved by ' + User1 + ', but NOT by ' + User2 + ':')
    C = 0
    for k in range(len(Lst1)):
        if(not Lst1[k] in Lst2):
             C += 1
             print ('\t' + str(Lst1[k]))
    print (str(C) + ' Challenges have been solved by ' + User1 + ' BUT NOT by ' + User2)

    print ('\nChallenges solved by ' + User2 + ', but NOT by ' + User1 + ':')
    C = 0
    for k in range(len(Lst2)):
        if(not Lst2[k] in Lst1):
             C += 1
             print ('\t' + str(Lst2[k]))
    print (str(C) + ' Challenges have been solved by ' + User2 + ' BUT NOT by ' + User1)

def ShowUserInfo():
    MsgGetUser = 'Enter the ID or username: '
    User = input(MsgGetUser)

    r = requests.get(APIURLUserInfo.format(user=User))
    if(r.status_code == 200):
        user = r.json()
        print('ID: {}'.format(user['user'][0]['id']))
        print('User: {}'.format(user['user'][0]['username']))
        print('Profile: {}/profile/{}/{}'.format(URL, user['user'][0]['id'], user['user'][0]['username']))

    else:
        raise Exception('Request failed')

def ShowUserScore():
    MsgGetUser = 'Enter the ID or username: '
    UserID = input(MsgGetUser)

    try:
        int(UserID)
        Tmp = requests.get(APIURLUserInfo.format(user=UserID)).text
        UserName = (Tmp[Tmp.find("\"username\":\"")+12:Tmp.find("\"}]}")])
    except :
        UserName = UserID
        Tmp = requests.get(APIURLUserInfo.format(user=UserID)).text
        if Tmp.lower().find(str(UserID).lower()) == -1:
            print('\nOups! User ' + UserID + ' not found!')
            sys.exit(1)

    r = requests.get(APIURLUserScore.format(userid=UserID))
    if(r.status_code == 200):
        user = r.json()

        print("WARNING: This API call has some issues and therefore, the data could be false.")
        print('Username: {}'.format(UserName))
        print('ID: {}'.format(user['user']))
        print('Score: {score}/{maxScore}'.format(score=user['score'], maxScore=user['maxscore']))
        print('Rank: {rank}/{totalPlayers}'.format(rank=user['rank'], totalPlayers=user['totalplayers']))
        print('Solved: {solved}/{totalChallenges}'.format(solved=user['solved'], totalChallenges=user['totalchallenges']))
        print('Profile: {}/profile/{}/{}'.format(URL, user['user'], UserName))

    else:
        raise Exception('Request failed')


def ShowChallengeInfo():
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    
    ChallengeID = int(input(MsgGetChallengeID))

    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    if(r.status_code == 200):
        challenge = r.json()

        print('ID: {}'.format(challenge['challenge']['id']))
        print('Title: {}'.format(challenge['challenge']['title']))
        print('Category: {}'.format(challenge['challenge']['category']))
        print('Points: {}'.format(challenge['challenge']['points']))
        print('Author: {}'.format(challenge['challenge']['author']))
        print('Last Submit: {}'.format(challenge['challenge']['lastSubmit']))
        print('Validated: {}'.format(challenge['challenge']['validated']))
    else:
        raise Exception('Request failed')

def ListUsersByChallenge():
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    
    ChallengeID = int(input(MsgGetChallengeID))

    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    if(r.status_code == 200):
        challenge = r.json()
        if(challenge['success'] == 1):
            print('Challange: {}'.format(challenge['challenge']['category']) + ' / {}'.format(challenge['challenge']['title']))
            r = requests.get(APIURLListUserByChallenge.format(challengeid=ChallengeID))
            if(r.status_code == 200):
                challenger = r.json()
                print('Solved by: \n\t{}'.format('\n\t'.join([a for a in sorted(challenger['solved'])])))
                print('Number of solves: {}'.format(len(challenger['solved'])))
            else:
                raise Exception('Request failed')

def ListWriteUpByChallenge():
    MsgGetChallengeID = 'Enter the ID of the challenge: '
    ChallengeID = int(input(MsgGetChallengeID))
    r = requests.get(APIURLChallengeInfo.format(challengeid=ChallengeID))
    if(r.status_code == 200):
        challenge = r.json()
        if(challenge['success'] == 1):
            print('Challange: {}'.format(challenge['challenge']['category']) + ' / {}'.format(challenge['challenge']['title']))
            r = requests.get(APIURLListWhoMadeWriteUp.format(challengeid=ChallengeID))
            if(r.status_code == 200):
                challenger = r.json()
                print('Write up made by:')
                WriteUp = list()
                for User in range(len(challenger['writeup'])):
                    if(int(challenger['writeup'][User]['specialmention']) == 1):
                        WriteUp.append('\t{0:20}{1}'.format(challenger['writeup'][User]['user'],'Special mention'))
                    else:
                        WriteUp.append('\t{}'.format(challenger['writeup'][User]['user']))
                WriteUp = (sorted(WriteUp))
                for User in range(len(WriteUp)):
                    print(WriteUp[User])
                print('Number of write up: {}'.format(len(challenger['writeup'])))
            else:
                raise Exception('Request failed')
        else:
            raise Exception('Challenge does not exist!')
    else:
        raise Exception('Request failed')

if __name__=='__main__':
    try:
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
            ListUsersByChallenge()
        if(Choice == 6):
            ListWriteUpByChallenge()
        if(Choice == 0):
            raise Exception('Thank for using this script')
    except Exception as e:
        print(e)
        sys.exit(1)

