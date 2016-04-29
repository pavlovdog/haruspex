from pymongo import MongoClient
import vk
import time

# connect to Mongo, get access token, client secret, profile's id, next_ url (0)
client = MongoClient()
usersDB = client["users"]["full"]
finalDB = client["users"]["vk"]

session = vk.Session()
api = vk.API(session)

fields = [	'photo_id', 'sex', 'bdate', 'city', 
			'country', 'home_town', 'photo_100', 'lists', 
			'domain', 'contacts', 'site', 'education', 
			'universities', 'schools', 'status', 'followers_count', 
			'occupation', 'nickname', 'relatives', 'relation', 
			'personal', 'connections', 'exports', 'wall_comments', 
			'activities', 'interests', 'music', 'movies', 
			'tv', 'books', 'games', 'about', 
			'quotes', 'timezone', 'screen_name', 
			'career', 'military']

# have smth like ".../vk.com/..." in "website" field and not parsed yet
# print usersDB.find({"external_url" : {"$regex" : "/vk.com/"}, "VK_parsed" : None}).count()

for user in usersDB.find({"external_url" : {"$regex" : "/vk.com/"}, "VK_parsed" : None}):
	if not finalDB.find_one({"username" : user["username"]}):
		user_id = user["external_url"].encode('utf8').split('/')[-1] or user["external_url"].encode('utf8').split('/')[-2]
		print "USER-ID {}; INSTAGRAM USERNAME {}".format(user_id, user["username"].encode('utf8'))

		try:
			# get data about current user
			userVK = api.users.get(user_ids = user_id, fields = fields)
			user.update(userVK[0])
			finalDB.insert(user)
			usersDB.update({"username" : user["username"]}, {"$set" : {"VK_parsed" : True}})
			print userVK
		except Exception as e:
			print e
			time.sleep(2)