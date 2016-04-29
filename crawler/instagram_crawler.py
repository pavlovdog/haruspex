from pymongo import MongoClient
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import json

# INIT
def user_info(user):
    r = requests.get("https://www.instagram.com/{}/".format(user["username"]))

    html_code = r.text

    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        script = soup.find_all('script')[6].string
        data = json.loads(script[21:-1])
        r = data["entry_data"]["ProfilePage"][0]["user"]

        if r["is_private"]:
            # print "Exception: account is private"
            return False
        
        if not r["external_url"]:
            # print "Exception: not external url"
            return False
        
        if not "vk.com" in r["external_url"]:
            # print "Exception: url doesn't look like '...vk.com...'"
            return False
                
        r["follows"] = r["follows"]["count"]
        r["followed_by"] = r["followed_by"]["count"]
        r["media_count"] = r["media"]["count"]
        r["_id"] = r["id"]
        
        if r["media_count"] == 0:
            # print "Exception: no media"
            return False
        
        if r["follows"] > 1000:
            # print "Exception: too many follows"
            return False
        
        if r["followed_by"] > 1000:
            # print "Exception: too many followers"
            return False

        
        keys_to_delete = ["profile_pic_url_hd", "requested_by_viewer", "country_block",
                         "blocked_by_viewer", "has_blocked_viewer", "has_requested_viewer",
                         "is_verified", "is_private", "follows_viewer", "followed_by_viewer"]
        for key in keys_to_delete:
            r.pop(key, None)

        # print type(r)
        
        users_instagram_info.update({"_id" : r["_id"]}, r, True)
        return True
    except Exception as e:
        print e
        return False

client = MongoClient(connect = False)
users_instagram = client["project"]["targets"]
users_instagram_info = client["project"]["instagram_info"]
url = "https://www.instagram.com/{}/"
p = Pool(10)

def parse_users():
    limit = 10000
    offset = 0

    while offset != 5000000:
        users = list(users_instagram.find().skip(offset).limit(limit))
        # p.map(user_info, users)
        print "CRAWLERED USERS FROM {} TO {}".format(offset, offset + limit)
        print users[0]
        print '========================='
        offset += limit

parse_users()
