#!/usr/bin/env python3

'''

 Initial version by: jusb3
 Rewrote by        : TheIndian, July 4th, 2019
 Redistribution authorized by jusb3
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

'''

import re, sys
import urllib.request as urllib

Msg1 = 'Enter the name of user 1: '
Msg2 = 'Enter the name of user 2: '
URL  = 'https://ringzer0ctf.com'

User1 = input(Msg1)
User2 = input(Msg2)

print ('Compare users ' + User1 + ' vs ' + User2)


print (' Get profile ID of ' + User1 + '. Please wait.')
Tmp = str(urllib.urlopen(URL+"/api/user/"+User1).read())
if Tmp.lower().find(str(User1).lower()) == -1:
    print('\nOups! User 1 ' + User1 + ' not found!')
    exit()
User1 = Tmp[Tmp.find("username\":\"")+11:Tmp.find("\"}]}")]
ID1 = Tmp[Tmp.find("\"id\":\"")+6:Tmp.find("\",\"username")]

print (' Get profile ID of ' + User2 + '. Please wait.')
Tmp = str(urllib.urlopen(URL+"/api/user/"+User2).read())
if Tmp.lower().find(str(User2).lower()) == -1:
    print('\nOups! User 2 ' + User2 + ' not found!')
    exit()
User2 = Tmp[Tmp.find("username\":\"")+11:Tmp.find("\"}]}")]
ID2 = Tmp[Tmp.find("\"id\":\"")+6:Tmp.find("\",\"username")]


print (' Get Challanges made by ' + User1 + '. Please wait.')
Tmp = urllib.urlopen(URL+'/profile/'+ID1).read()
Lst1 = re.findall(b'><div style="width: 150px; display: inline-block"><b>(\S*.*)',Tmp); Lst1.sort()
for i in range(len(Lst1)):
    Lst1[i] = str(Lst1[i]).replace("</a>'","").replace("</a>\"","").replace("</b></div>"," / ").replace("b'","").replace("b\"","")

print (' Get Challanges made by ' + User2 + '. Please wait.')
Tmp = urllib.urlopen(URL+'/profile/'+ID2).read()
Lst2 = re.findall(b'><div style="width: 150px; display: inline-block"><b>(\S*.*)',Tmp); Lst2.sort()
for i in range(len(Lst2)):
    Lst2[i] = str(Lst2[i]).replace("</a>'","").replace("</a>\"","").replace("</b></div>"," / ").replace("b'","").replace("b\"","")


print ('\nSames Challenges solved by ' + User1 + ' AND by ' + User2 + ':')
C = 0
for k in range(len(Lst2)):
    if Lst2[k] in Lst1:
         C += 1
         print ('\t' + str(Lst2[k]))
print (str(C) + ' sames Challenges has been solved by ' + User1 + ' AND by ' + User2)

print ('\nChallenges solved by ' + User1 + ', but NOT by ' + User2 + ':')
C = 0
for k in range(len(Lst1)):
    if(not Lst1[k] in Lst2):
         C += 1
         print ('\t' + str(Lst1[k]))
print (str(C) + ' Challenges has been solved by ' + User1 + ' BUT NOT by ' + User2)


print ('\nChallenges solved by ' + User2 + ', but NOT by ' + User1 + ':')
C = 0
for k in range(len(Lst2)):
    if(not Lst2[k] in Lst1):
         C += 1
         print ('\t' + str(Lst2[k]))
print (str(C) + ' Challenges has been solved by ' + User2 + ' BUT NOT by ' + User1)


