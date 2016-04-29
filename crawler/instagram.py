from pymongo import MongoClient
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import json

# INIT
def user_info(html_code):
    # try:
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
    # except Exception:
    	print Exception
    #     return None

client = MongoClient()
instagram_data = client["project"]["instagram_data"]
url = "https://www.instagram.com/{}/"

r = requests.get(url.format("14photos"))

# print r.text.encode("utf8")

data = user_info(r.text)

print data
