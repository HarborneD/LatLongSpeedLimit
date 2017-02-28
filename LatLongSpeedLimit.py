import urllib.request

api_key = "AIzaSyA-LgIcJAnUzw_BUveV6fRQwUKVvCxbkp8"

path = "38.75807927603043,-9.03741754643809|38.6896537,-9.1770515|41.1399289,-8.6094075"

url = "https://roads.googleapis.com/v1/speedLimits"


api_request = url + "?path="+path+"&key="+api_key

print(api_request)
speed_limits = urllib.request.urlretrieve(api_request)


print(speed_limits)
