import pickle
import requests
from bs4 import BeautifulSoup
import json

def get_user_info(username):
    r = requests.get("http://instagram.com/" + username)
    html_code = r.text

    try:
        soup = BeautifulSoup(html_code, 'html.parser')
        script = soup.find_all('script')[6].string
        data = json.loads(script[21:-1])
        r = data["entry_data"]["ProfilePage"][0]["user"]
        if r["is_private"]:
            print "Private"
            return None
        r["follows"] = r["follows"]["count"]
        r["followed_by"] = r["followed_by"]["count"]
        r["media_count"] = r["media"]["count"]
        return r
    except:
        print "error"
        return None

def make_user_features(info):
    pass

def user_predict_sex(features):
    pass

def user_predict_age(features):
    pass

if __name__ == "__main__":
    print get_user_info("kugusha")