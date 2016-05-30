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
    try:
        features["average_lenght_caption"] = np.mean([len(i["caption"]) for i in info["media"]["nodes"]])
    except:
        features["average_lenght_caption"] = 0
    
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
    a = {u'username': u'black_kulich', u'has_blocked_viewer': False, 'media_count': 242, u'follows': 285, u'requested_by_viewer': False, u'followed_by': 461, u'external_url_linkshimmed': None, u'has_requested_viewer': False, u'country_block': None, u'follows_viewer': False, u'profile_pic_url_hd': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-19/s320x320/12407186_1721462848142926_2029080054_a.jpg', u'profile_pic_url': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-19/s150x150/12407186_1721462848142926_2029080054_a.jpg', u'is_private': False, u'full_name': None, u'media': {u'count': 242, u'page_info': {u'has_previous_page': False, u'start_cursor': u'1261632322374209858', u'end_cursor': u'1234200521209024731', u'has_next_page': True}, u'nodes': [{u'code': u'BGCN-msRBFC', u'dimensions': {u'width': 1080, u'height': 1294}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 1}, u'caption': u'\u0421\u0434\u0430\u043b\u0430 \u043f\u0440\u043e\u0435\u043a\u0442, \u0430 \u044d\u043a\u0437\u0430\u043c\u0435\u043d\u043e\u0432 \u043c\u0435\u043d\u044c\u0448\u0435 \u043d\u0435 \u0441\u0442\u0430\u043b\u043e\U0001f605 #\u0444\u043a\u043d', u'likes': {u'count': 49}, u'date': 1464618314, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.107.1080.1080/13248954_579871228839831_673284056_n.jpg?ig_cache_key=MTI2MTYzMjMyMjM3NDIwOTg1OA%3D%3D.2.c', u'is_video': False, u'id': u'1261632322374209858', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13248954_579871228839831_673284056_n.jpg?ig_cache_key=MTI2MTYzMjMyMjM3NDIwOTg1OA%3D%3D.2'}, {u'code': u'BFpMfMARBAw', u'dimensions': {u'width': 480, u'height': 599}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 3}, u'caption': u'\u0412\u0435\u0441\u0451\u043b\u043e\u0439 \u043d\u043e\u0447\u0438 \U0001f319', u'likes': {u'count': 110}, u'date': 1463778672, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/c0.79.637.637/13181364_513644645509698_452063184_n.jpg?ig_cache_key=MTI1NDU4ODg5MDk1MDY2ODMzNg%3D%3D.2.c', u'is_video': False, u'id': u'1254588890950668336', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/p480x480/13181364_513644645509698_452063184_n.jpg?ig_cache_key=MTI1NDU4ODg5MDk1MDY2ODMzNg%3D%3D.2'}, {u'code': u'BFcD8EcRBKZ', u'dimensions': {u'width': 1080, u'height': 1080}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 1}, u'caption': u'\u0421\u043f\u0430\u0441\u0438\u0431\u043e \u0437\u0430 \u0447\u0443\u0434\u0435\u0441\u043d\u044b\u0439 \u0431\u0443\u043a\u0435\u0442\U0001f607', u'likes': {u'count': 85}, u'date': 1463337982, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/13108912_213331635720531_1055591525_n.jpg?ig_cache_key=MTI1MDg5MjExODU3OTQ4MzI4OQ%3D%3D.2', u'is_video': False, u'id': u'1250892118579483289', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13108912_213331635720531_1055591525_n.jpg?ig_cache_key=MTI1MDg5MjExODU3OTQ4MzI4OQ%3D%3D.2'}, {u'code': u'BFW_OVNRBFb', u'dimensions': {u'width': 1080, u'height': 1349}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 3}, u'caption': u'\u0412\u043e\u0442 \u0441\u0432\u044f\u0436\u0438\u0441\u044c \u0441 \u0431\u0430\u0431\u0430\u043c\u0438 \u0440\u0430\u0437\u0433\u043e\u0432\u0430\u0440\u0438\u0432\u0430\u0442\u044c, \u043d\u0435 \u0441\u043e\u0433\u0440\u0435\u0448\u0430, \u0441\u043e\u0433\u0440\u0435\u0448\u0438\u0448\u044c. (\u0441) \u041e\u0441\u0442\u0440\u043e\u0432\u0441\u043a\u0438\u0439', u'likes': {u'count': 103}, u'date': 1463167738, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/13183555_1749996285279950_1723780216_n.jpg?ig_cache_key=MTI0OTQ2NDAwODQxNTkwODE4Nw%3D%3D.2.c', u'is_video': False, u'id': u'1249464008415908187', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13183555_1749996285279950_1723780216_n.jpg?ig_cache_key=MTI0OTQ2NDAwODQxNTkwODE4Nw%3D%3D.2'}, {u'code': u'BFMlLvuRBAQ', u'dimensions': {u'width': 1080, u'height': 1349}, u'comments': {u'count': 2}, u'owner': {u'id': u'29114355'}, u'likes': {u'count': 99}, u'date': 1462818541, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/13130031_1729770063969652_328584661_n.jpg?ig_cache_key=MTI0NjUzNDczMTc1MjAxNzkzNg%3D%3D.2.c', u'is_video': False, u'id': u'1246534731752017936', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13130031_1729770063969652_328584661_n.jpg?ig_cache_key=MTI0NjUzNDczMTc1MjAxNzkzNg%3D%3D.2'}, {u'code': u'BFFtaNvRBIk', u'dimensions': {u'width': 1080, u'height': 1349}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 1}, u'caption': u"Hangin' with some girls \U0001f51b", u'likes': {u'count': 110}, u'date': 1462587973, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/13129885_1737521883151414_144137546_n.jpg?ig_cache_key=MTI0NDYwMDU4NTU4ODgzODk0OA%3D%3D.2.c', u'is_video': False, u'id': u'1244600585588838948', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13129885_1737521883151414_144137546_n.jpg?ig_cache_key=MTI0NDYwMDU4NTU4ODgzODk0OA%3D%3D.2'}, {u'code': u'BE6pCC0RBEX', u'dimensions': {u'width': 1080, u'height': 930}, u'comments': {u'count': 0}, u'owner': {u'id': u'29114355'}, u'likes': {u'count': 86}, u'date': 1462216579, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c75.0.930.930/13126704_269921546680172_1118640334_n.jpg?ig_cache_key=MTI0MTQ4NTEwNzY2NDI2MTM5OQ%3D%3D.2.c', u'is_video': False, u'id': u'1241485107664261399', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13126704_269921546680172_1118640334_n.jpg?ig_cache_key=MTI0MTQ4NTEwNzY2NDI2MTM5OQ%3D%3D.2'}, {u'code': u'BE3uMN6RBE6', u'dimensions': {u'width': 1080, u'height': 1255}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 4}, u'caption': u'\u041f\u043e\u043a\u0430 \u043c\u0430\u043c\u0430 \u043d\u0435 \u0432\u0438\u0434\u0438\u0442 \U0001f602', u'likes': {u'count': 90}, u'date': 1462118620, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.87.1080.1080/13129706_227714154264168_330802268_n.jpg?ig_cache_key=MTI0MDY2MzM3MjA3MzI3NTcwNg%3D%3D.2.c', u'is_video': False, u'id': u'1240663372073275706', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13129706_227714154264168_330802268_n.jpg?ig_cache_key=MTI0MDY2MzM3MjA3MzI3NTcwNg%3D%3D.2'}, {u'code': u'BE0r6eJRBFH', u'dimensions': {u'width': 1080, u'height': 1349}, u'comments': {u'count': 7}, u'owner': {u'id': u'29114355'}, u'likes': {u'count': 94}, u'date': 1462016763, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/13092365_1700644896870288_227989956_n.jpg?ig_cache_key=MTIzOTgwODkzMTUzMTA2NzcxOQ%3D%3D.2.c', u'is_video': False, u'id': u'1239808931531067719', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13092365_1700644896870288_227989956_n.jpg?ig_cache_key=MTIzOTgwODkzMTUzMTA2NzcxOQ%3D%3D.2'}, {u'code': u'BEy55-hxBID', u'dimensions': {u'width': 1080, u'height': 1349}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 0}, u'caption': u'Munich \U0001f37b\u2600\ufe0f', u'likes': {u'count': 76}, u'date': 1461956990, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/13117989_245536159133766_891437048_n.jpg?ig_cache_key=MTIzOTMwNzUyMDI4MDEwNTQ3NQ%3D%3D.2.c', u'is_video': False, u'id': u'1239307520280105475', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/13117989_245536159133766_891437048_n.jpg?ig_cache_key=MTIzOTMwNzUyMDI4MDEwNTQ3NQ%3D%3D.2'}, {u'code': u'BElQ08vxBLZ', u'dimensions': {u'width': 1080, u'height': 1349}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 5}, u'caption': u"\U0001f3a7 A$AP Rocky-Fuckin' Problems(Jawster Remix) #np", u'likes': {u'count': 104}, u'date': 1461499246, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/12940051_281235182215677_468166140_n.jpg?ig_cache_key=MTIzNTQ2NzY4MDE2NTkyNTU5Mw%3D%3D.2.c', u'is_video': False, u'id': u'1235467680165925593', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/12940051_281235182215677_468166140_n.jpg?ig_cache_key=MTIzNTQ2NzY4MDE2NTkyNTU5Mw%3D%3D.2'}, {u'code': u'BEgwtXARBDb', u'dimensions': {u'width': 1080, u'height': 955}, u'owner': {u'id': u'29114355'}, u'comments': {u'count': 4}, u'caption': u'\u041a\u043e\u0433\u0434\u0430 \u0441\u0434\u0430\u043b \u0432\u0441\u0435 \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u044b', u'likes': {u'count': 87}, u'date': 1461348188, u'thumbnail_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c62.0.955.955/12724911_231635347196534_1301584642_n.jpg?ig_cache_key=MTIzNDIwMDUyMTIwOTAyNDczMQ%3D%3D.2.c', u'is_video': False, u'id': u'1234200521209024731', u'display_src': u'https://scontent-frt3-1.cdninstagram.com/t51.2885-15/e35/12724911_231635347196534_1301584642_n.jpg?ig_cache_key=MTIzNDIwMDUyMTIwOTAyNDczMQ%3D%3D.2'}]}, u'blocked_by_viewer': False, u'followed_by_viewer': False, u'is_verified': False, u'id': u'29114355', u'biography': u'Dasha\U0001f60a', u'external_url': None}
    print make_user_features(a)