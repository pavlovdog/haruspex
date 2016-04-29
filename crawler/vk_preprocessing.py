from pymongo import MongoClient

client = MongoClient()
vk = client["users"]["vk"]
vk_dataset = client["users"]["vk_dataset"]
vk_dataset.drop()

for user in vk.find():
	print "USER - {}".format(user["username"].encode("utf-8"))

	check_bday = False
	check_followings = False
	check_followers = False
	check_media = False
	check_sex = False
    
    # Sex is 1 or 2
	try:
		check_sex = user["sex"] == 2 or user["sex"] == 1
	except:
		check_sex = False
    
	# Bday like "dd.mm.yyyy" and less than 50 years
	try:
		check_bday = user["bdate"].count(".") == 2
		check_bday = check_bday and int(user["bdate"].split(".")[2]) > 1970
	except:
		check_bday = False

	# Followings less than 700 and more than 30
	try:
		check_followings = 30 < user["follows"]["count"] < 700
	except:
		check_followings = False

	# Followers more than 50 and less than 1500
	try:
		check_followers = 50 < user["followed_by"]["count"] < 1500
	except:
		check_followers = False

	# Media more than 12 and less than 1000
	try:
		check_media = 12 <= user["media"]["count"] < 1000
	except:
		check_media = False

	print "MEDIA - {}, FOLLOWERS - {}, FOLLOWINGS - {}, BDAY - {}".format(check_media, check_followers, check_followings, check_bday)

	if check_media and check_followers and check_followings and check_bday and not user["is_private"] and check_sex:
		print "ADDED"
		vk_dataset.insert(user)
	print "================================================"