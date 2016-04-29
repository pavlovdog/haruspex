import requests
import csv
import pickle
import random
import os
import json
from pymongo import MongoClient
from multiprocessing import Pool

ACCESS_TOKENS = [
    "1259584025.2974fce.8ba9c3c4933c4f5dabe6cc211432d03e",
	"2206388144.2974fce.3fd62b4f3d604c25b788d5014e2d19e6",
	"2867962189.2974fce.d21677320737472abafa9e72988b8a5c",
	"3104427830.2974fce.1bac839ee4794f3297305ff316e85228",
	"3062014845.2974fce.f7861ce24f8b42e09db207b39b9151fb"
]

def parse_target(target, opts):
    s = requests.Session()
    db = MongoClient().project
    cnt = 0
    uid = opts["id"]
    c_access_token = 0
    url = "https://api.instagram.com/v1/users/{}/followed-by?count=1000&access_token={}".format(uid, ACCESS_TOKENS[c_access_token])
    while url:
        r = s.get(url).json()
        code = r.get("code", 0)
        if code != 0:
            if code == 429:
                print("access_token rate limit exceeded, trying new token")
                c_access_token += 1
                if c_access_token >= len(ACCESS_TOKENS):
                    print("no more access_tokens, finishing :(")
                    print("added {} users from '{}'".format(cnt, target))
                    break
                else:
                    url = url.replace(ACCESS_TOKENS[c_access_token - 1], ACCESS_TOKENS[c_access_token])
                    continue
            else:
                print("error:", r["error_message"])
                break
        pagination = r.get("pagination", {})
        if "next_url" in pagination:
            url = r["pagination"]["next_url"]
        else:
            url = None
        for user in r["data"]:
            res = db.targets.update({"_id": user["id"]}, {"_id": user["id"], "username": user["username"]}, True)
            if not res["updatedExisting"]:
                cnt += 1
            if cnt % 500 == 0 and cnt > 0:
                print("added {} users from '{}'".format(cnt, target))

def dump_targets():
    db = MongoClient().project
    with open("targets_users.json", "w") as f:
        r = []
        for user in db.targets.find():
            r.append(user)
        json.dump({"users": r}, f)

def update_targets():
    with open("target.json") as f:
        targets = json.load(f)
        p = Pool(9)
        w = []
        for target, opts in targets.items():
            w.append(p.apply_async(parse_target, (target, opts)))
            print target, opts
        # for t in w:
        #     t.get()

update_targets()
