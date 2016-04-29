from pymongo import MongoClient
import numpy as np
import time
import datetime
import random
import re

client = MongoClient()
vk = client["users"]["vk_dataset"]

def load_vk():
	return vk_data

def count_followings():
	vk_data = vk.find()
	response = np.array([])
	for record in vk_data:
		try:
			response = np.append(response, record["follows"]["count"])
		except:
			response = np.append(response, 0)

	return response

def count_followers():
	vk_data = vk.find()
	response = np.array([])
	for record in vk_data:
		try:
			response = np.append(response, record["followed_by"]["count"])
		except:
			response = np.append(response, 0)

	return response

def count_media():
	vk_data = vk.find()
	response = np.array([])
	for record in vk_data:
		try:
			response = np.append(response, record["media"]["count"])
		except:
			response = np.append(response, 0)

	return response

def list_ages():
	vk_data = vk.find()
	response = np.array([])
	for record in vk_data:
		try:
			bday = record["bdate"]
			if bday.count(".") == 2:
				date_object = datetime.datetime.strptime(bday, '%d.%m.%Y')
				response = np.append(response, 2016 - date_object.year)
			else:
				response = np.append(response, 0)
		except:
			response = np.append(response, 0)

	return response

def list_usernames():
	vk_data = vk.find()
	response = np.array([])
	for record in vk_data:
		try:
			response = np.append(response, record["username"])
		except:
			response = np.append(response, "No name")

	return response

def average_likes():
    vk_data = vk.find()
    response = np.array([])

    for record in vk_data:
        try:
            media_nodes = record["media"]["nodes"]
            user_average = np.mean([i["likes"]["count"] for i in media_nodes])
            response = np.append(response, user_average)
        except:
            response = np.append(response, 0)
    return response
                 
def average_comments():
    vk_data = vk.find()
    response = np.array([])

    for record in vk_data:
        try:
            media_nodes = record["media"]["nodes"]
            user_average = np.mean([i["comments"]["count"] for i in media_nodes])
            response = np.append(response, user_average)
        except:
            response = np.append(response, 0)
    return response

def list_sex():
    vk_data = vk.find()
    response = np.array([])

    for record in vk_data:
        try:
            response = np.append(response, record["sex"] - 1)
        except:
            response = np.append(response, random.choice([1.0, 0.0]))

    return response

def average_lenght_caption():
    vk_data = vk.find()
    response = np.array([])
    captions = np.array([])

    for record in vk_data:
    	try:
    		media_nodes = record["media"]["nodes"]
    		user_average = np.mean([len(i["caption"]) for i in media_nodes])
    		response = np.append(response, user_average)
    	except:
    		response = np.append(response, 0)

    return response

def average_smileys():
    vk_data = vk.find()
    response = np.array([])

    for record in vk_data:
        smileys = []
        try:
            media_nodes = record["media"]["nodes"]
            for media in media_nodes:
                if "caption" in media.keys():
                    smileys.append(len(re.findall(u'[\U0001f600-\U0001f650]', media["caption"])))
            if smileys == []:
                smileys = [0]
            response = np.append(response, np.mean(smileys))
        except Exception as e:
            reponse = np.append(response, 0)
    return response

def media_frequency():
    vk_data = vk.find()
    response = np.array([])
    
    for record in vk_data:
        frequency_array = []
        try:
            media_nodes = record["media"]["nodes"]
            for media in media_nodes[::-1]:
                frequency_array.append(media["date"])
            frequency_array = np.diff(frequency_array)
            frequency_array = [datetime.datetime.fromtimestamp(i).day*24 + datetime.datetime.fromtimestamp(i).hour for i in frequency_array]
            response = np.append(response, np.mean(frequency_array))
        except:
            response = np.append(response, 0)
#         break
    return response

def video_number():
    vk_data = vk.find()
    response = np.array([])
    
    for record in vk_data:
        video_counter = 0
        try:
            media_nodes = record["media"]["nodes"]
            for media in media_nodes:
                video_counter += media["is_video"]
            response = np.append(response, video_counter)
        except:
            response = np.append(response, 0)
            
    return response

def list_ages_classes():
    ages = list_ages()
    response = np.array([])
    
    for age in ages:
        if age < 15:
            response = np.append(response, 0)
        elif 15 <= age < 25:
            response = np.append(response, 1)
        elif 25 <= age < 35:
            response = np.append(response, 2)
        elif 35 <= age < 45:
            response = np.append(response, 3)
        else:
            response = np.append(response, 4)
            
    return response