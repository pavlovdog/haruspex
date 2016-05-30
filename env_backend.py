import pickle
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import datetime
import re

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
    features = {}

    features["count_followings"] = info["follows"]
    features["count_followers"] = info["followed_by"]
    features["count_media"] = info["media_count"]
    features["average_likes"] = np.mean([i["likes"]["count"] for i in info["media"]["nodes"]])
    features["average_comments"] = np.mean([i["comments"]["count"] for i in info["media"]["nodes"]])
    features["average_lenght_caption"] = np.mean([len(i["caption"]) for i in info["media"]["nodes"]])
    features["media_frequency"] = get_media_frequency(info)
    features["video_number"] = get_video_number(info)
    features["average_smileys"] = get_average_smileys(info)

    return features

    
def user_predict(features):
    with open("models/sex_model.pkl") as f:
        classifier_sex = pickle.load(f)

    with open("models/age_model.pkl") as f:
        classifier_age = pickle.load(f)

    data = [features["count_followers"],
            features["count_followings"],
            features["count_media"],
            features["average_likes"],
            features["average_comments"],
            features["average_lenght_caption"],
            features["average_smileys"],
            features["media_frequency"],
            features["video_number"]]

    return {
        "sex" : classifier_sex.predict(data)[0],
        "age" : classifier_age.predict(data)[0]
    }

def get_video_number(info):
    counter = 0
    for media in info["media"]["nodes"]:
        counter += media["is_video"]
    return counter

def get_media_frequency(info):
    frequency_array = []
    for media in info["media"]["nodes"]:
        frequency_array.append(media["date"])
    frequency_array = np.diff(frequency_array)
    frequency_array = [datetime.datetime.fromtimestamp(i).day*24 + datetime.datetime.fromtimestamp(i).hour for i in frequency_array]
    return np.mean(frequency_array)

def get_average_smileys(info):
    smileys = []
    for media in info["media"]["nodes"]:
        if "caption" in media.keys():
            smileys.append(len(re.findall(u'[\U0001f600-\U0001f650]', media["caption"])))
    if not smileys:
        smileys = [0]

    return np.mean(smileys)

if __name__ == "__main__":
    a = {'count_followings': 185, 'count_followers': 675, 'average_lenght_caption': 46.583333333333336, 'average_comments': 2.4166666666666665, 'media_frequency': 717.36363636363637, 'average_smileys': 0.083333333333333329, 'count_media': 289, 'video_number': 0, 'average_likes': 101.0}
    # print user_predict_sex(a.values())
    data = [a["count_followers"],
            a["count_followings"],
            a["count_media"],
            a["average_likes"],
            a["average_comments"],
            a["average_lenght_caption"],
            a["average_smileys"],
            a["media_frequency"],
            a["video_number"]]
    print user_predict_sex([data])
