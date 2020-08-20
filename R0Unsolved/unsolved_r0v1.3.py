#!/usr/bin/python3
#
# 20xx-xx-xxv1.0: Initial version - (by dysleixa)
# 2019-11-14v1.1: Could specify username or user ID instead just user ID (by TheIndian)
# 2019-11-17v1.2: Display category of Challenges (by TheIndian)
# 2020-06-17v1.3: Use the new API to get user information

DESCRIPTION = """Lists the unsolved challenges on R0 (using the given user ID),
sorted to help pick the next unsolved challenge that has the most solves,
weighted by points.
"""

import argparse
import collections
import re
from bs4 import BeautifulSoup
from requests import get
from tabulate import tabulate
from urllib.parse import urljoin
import urllib.request as urllib
import sys

URL  = 'https://ringzer0ctf.com'
Msg1 = 'Enter the name of user: '
APIURLUserInfo = URL + '/api/user/info/{userid}'

Challenge = collections.namedtuple(
        "Challenge", "id name category points solves")

BASE_URL = "https://ringzer0ctf.com/"

def parse_category_name(category_text):
    """Parses something like 'Coding Challenges (17 / 17)' to only return the
    name of the category."""
    match = re.match(r'(.*?)\s*\(.*', category_text)
    assert match is not None and len(match.groups()) >= 1,\
           "Format of category header unexpected: '%s'" % category_text
    return match.groups()[0]
assert parse_category_name("Cryptography (30 / 31)") == "Cryptography"

def parse_name(name_node):
    return name_node.get_text().strip()

def parse_id(url_node):
    url = url_node.attrs["href"]
    id_str = re.match(r".*/(\d+).*", url)
    return int(id_str.groups()[0])

def parse_challenge(challenge_row, category):
    name_node, points_node, solves_node = challenge_row.find_all('td')[:3]
    name = parse_name(name_node)
    id_ = parse_id(name_node.a)
    points = int(points_node.get_text())
    solves = int(solves_node.get_text())
    return Challenge(name=name, id=id_, points=points,
                     solves=solves, category=category)

def parse_category(category_node):
    challenges = []
    # special handling for Web's warning
    ssl_warning = category_node.find(id="ssl")
    if ssl_warning: ssl_warning.clear()  
    category_name = parse_category_name(category_node.get_text())

    table = category_node.find_next("table").tbody.extract()
    row = table.tr
    while row:
        challenges.append(parse_challenge(row, category_name))
        row = row.find_next("tr")
    return challenges

def fetch_all_challenges():
    r = get(urljoin(BASE_URL, "challenges"))
    assert r.status_code == 200

    challenges = []
    html = BeautifulSoup(r.text, "html.parser")
    for category in html.find_all(attrs={"data-id": True},
                                  class_="title_hover"):
        challenges.extend(parse_category(category))
    return challenges

def fetch_solved_challenge_ids(userid):
    r = get(urljoin(BASE_URL, "profile/%d" % userid))
    assert r.status_code == 200, "Couldn't fetch user profile for %d" % userid

    html = BeautifulSoup(r.text, "html.parser")
    ids = set()
    # There's a special mention writeup table too... Just try to parse any table
    for table in html.find_all("table"):
        for link_node in table.find_all("a"):
            # If we can extract a challenge for the <a> href, we consider that
            # this is a challenge ID.
            try:
                ids.add(parse_id(link_node))
            except: pass
    return ids

def challenge_score(challenge, points_weight):
    multiplier = (challenge.points - 1) * points_weight
    return challenge.solves * (1.0 + multiplier)

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("userid", default=0,
                         help="User ID (from your profile URL).")
    parser.add_argument("--points-weight", type=float, default=1.0,
                        help="Weight contributed by the challenge points to " +
                            "the sorting score.")
    parser.add_argument("-n", "--max-challenges", type=int, default=10,
                        help="Max number of challenges to display. " +
                            "Set to high number to display all.")
    args = parser.parse_args()
    r = get(APIURLUserInfo.format(userid=args.userid))
    r = r.json()
    if r['success'] == 0:
        print('\nOups!, user or ID \'{}\' not found!!!\n'.format(args.userid))
        sys.exit(1)
    print('\n Next suggested Challanges for \'{}\' (ID: {})\n'.format(r['data']['users'][0]['user']['username'], r['data']['users'][0]['user']['id']))

    try:
        int(args.userid)
        args.userid = int(args.userid)
    except:
        args.userid = int(r['data']['users'][0]['user']['id'])

    challenges = fetch_all_challenges()
    solved_ids = fetch_solved_challenge_ids(args.userid)
    unsolved = [chal for chal in challenges if chal.id not in solved_ids]
    points_weight = args.points_weight
    unsolved.sort(key=lambda chal: challenge_score(chal, points_weight),
                  reverse=True)
    display_n = args.max_challenges
    print(tabulate([[challenge_score(c, points_weight), c.category, c.name, c.id, c.solves,
                     c.points] for c in unsolved[:display_n]],
                   headers=["Score", "Category", "Name", "Id", "# Solves", "# Points"]))

if __name__ == "__main__":
    main()



