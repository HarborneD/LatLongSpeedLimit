import overpass

api = overpass.API()

cam_long = "5.6293520"

cam_lat = "50.5350159"

box_long = float(cam_long) - 0.01

box_lat = float(cam_lat) - 0.01

box_long2 = float(cam_lat) + 0.01

box_lat2 = float(cam_lat) + 0.01



map_query = overpass.MapQuery(box_long,box_lat,box_long2,box_lat2)
response = api.Get(map_query)

print(response)