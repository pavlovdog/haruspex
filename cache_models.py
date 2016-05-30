from env_data import *
import numpy as np
import pandas as pd
import sklearn
from pymongo import MongoClient
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

ages = list_ages()
followers = count_followers()
followings = count_followings()
media = count_media()
likes = average_likes()
comments = average_comments()
usernames = list_usernames()
sex = list_sex()
caption_lenght = average_lenght_caption()
smileys = average_smileys()
frequency = media_frequency()
video = video_number()
age_classes = list_ages_classes()

# Sex prediction
features_dataset = np.array([followers, followings, media, likes, comments, 
                        caption_lenght, smileys, frequency, video]).T

training_size = 0.7

features_training = features_dataset[:int(training_size*len(features_dataset))]
features_testing = features_dataset[int(training_size*len(features_dataset)):]

labels_training = sex[:int(training_size*len(features_dataset))]
labels_testing = sex[int(training_size*len(features_dataset)):]

classifier = DecisionTreeClassifier()
classifier.fit(features_training, labels_training)

with open("age_model.pkl", "w") as f:
	pickle.dump(classifier, f)