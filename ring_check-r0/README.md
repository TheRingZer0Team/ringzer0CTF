# ring_check

# Tool to get information about user's and challenges on RingZer0CTF.com
```
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
2020-12-20v4.1  : (by TheIndian)
                  New: Show write-up made by a user.
2023-07-21v4.2  : (by TheIndian)
                  Fix cosmetics
                  More interactive
                  Option 7: Show the user country RCEH status. Output can be sorted by date, users, country or RCEH
                  Work with the APIs changes on 2023-06 and fix APIs to return accurate info.

```
