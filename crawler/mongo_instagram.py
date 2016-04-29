from pymongo import MongoClient
from bs4 import BeautifulSoup
import json
import requests

# INIT
def user_info(html_code):
    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        script = soup.find_all('script')[6].string
        data = json.loads(script[21:-1])
        r = data["entry_data"]["ProfilePage"][0]["user"]
        if r["is_private"]:
            return None
        r["follows"] = r["follows"]["count"]
        r["followed_by"] = r["followed_by"]["count"]
        r["media_count"] = r["media"]["count"]
        return r
    except:
        return None

client = MongoClient()
all_users = client["project"]["all"]
instagram_users = client["project"]["instagram_data"]
requests = []

records = all_users.find({"filtered" : False}).limit(5000)

for record in records:
    requests.append(grequests.get("https://www.instagram.com/{}/".format(record["username"])))
    
print "================================"
print "Requests is ready, start mapping"
print "================================"

responses = grequests.map(requests)

for r in responses:
    try:
        print r
        if r.status_code == 200:
            info = user_info(r.text)
            if info:
                print "Adding - {}".format(info["username"])
                instagram_users.insert(info)
                all_users.update_one({"username" : info["username"]}, {"$set" : {"filtered" : True}})
    except:
        print r
