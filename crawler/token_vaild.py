from instagram.client import InstagramAPI

tokens = [	"1259584025.2974fce.8ba9c3c4933c4f5dabe6cc211432d03e",
			"2206388144.2974fce.3fd62b4f3d604c25b788d5014e2d19e6",
			"2867962189.2974fce.d21677320737472abafa9e72988b8a5c",
			"3104427830.2974fce.1bac839ee4794f3297305ff316e85228",
			"3062014845.2974fce.f7861ce24f8b42e09db207b39b9151fb"]

# for access_token in tokens:
# 	api = InstagramAPI(access_token = access_token)
# 	try:
# 		popular_media = api.media_popular(count=20)
# 		print "{} is okay".format(access_token)
# 	except InstagramAPIError as e:
# 		print e