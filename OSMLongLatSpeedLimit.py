import urllib.request
import xmltodict
import xml.etree.ElementTree as ET

import json

# camera_long2 = "5.6293520"

# camera_lat2 = "50.5350159"


# camera_long = "5.6276237"

# camera_lat = "50.5346803"

# api_url = 'http://www.overpass-api.de/api/xapi?*[maxspeed=*][bbox={long1},{lat1},{long2},{lat2}]'

# api_request = api_url.format(long1=camera_long,  lat1=camera_lat,long2=camera_long2,  lat2=camera_lat2)

# print(api_request)

# speed_limits = urllib.request.urlretrieve(api_request)
# print(speed_limits)

# road_speeds = {}

# tree = ET.parse(speed_limits[0])
# root = tree.getroot()

# for way in root.findall('way'):
# 	way_tags = way.findall('tag')
# 	max_speeds = [tag.attrib.get('v') for tag in way_tags if tag.attrib.get('k') == "maxspeed"]
# 	names = [tag.attrib.get('v') for tag in way_tags if tag.attrib.get('k') == "name"]
# 	road_speeds[names[0]] = max_speeds[0]	

# print(road_speeds)



def XMLfromOSMSpeedCall(long1,lat1,long2,lat2):
	api_url = 'http://www.overpass-api.de/api/xapi?*[maxspeed=*][bbox={long1},{lat1},{long2},{lat2}]'

	api_request = api_url.format(long1=long1,  lat1=lat1,long2=long2,  lat2=lat2)
	print(api_request)
	speed_limits = urllib.request.urlretrieve(api_request)

	return ET.parse(speed_limits[0])

def JSONfromTFLCall(camera_id):
	api_url = 'https://api.tfl.gov.uk/Place/JamCams_00001.{camera_id}'

	api_request = api_url.format(camera_id=camera_id)
	print(api_request)
	camera_api_response = urllib.request.urlretrieve(api_request)

	d = ""

	with open(camera_api_response[0]) as json_data:
		d = json.load(json_data)
		
	 
	return d

def OSMLongLatSpeedLimit(cam_long,cam_lat):
	box_long = str(float(cam_long) - 0.0002)

	box_lat = str(float(cam_lat) - 0.0002)

	box_long2 = str(float(cam_long) + 0.0002)

	box_lat2 = str(float(cam_lat) + 0.0002)

	tree = XMLfromOSMSpeedCall(box_long,box_lat,box_long2,box_lat2)

	road_speeds = {}

	unknown_counter = 0
	for way in tree.getroot().findall('way'):
		way_tags = way.findall('tag')
		for tag in way_tags:
			print(tag.attrib.get('k'),tag.attrib.get('v'))

		max_speeds = [tag.attrib.get('v') for tag in way_tags if tag.attrib.get('k') == "maxspeed"]
		names = [tag.attrib.get('v') for tag in way_tags if tag.attrib.get('k') == "name"]
		
		if(len(names) > 0 ):
			name= names[0]
		else:
			unknown_counter += 1
			name = "?-"+str(unknown_counter)


		if(len(max_speeds) > 0):
			road_speeds[name] = max_speeds[0]	
		else:
			road_speeds[name] = -1
	return road_speeds


#camera_long = "5.6293520"

#camera_lat = "50.5350159"

#print(OSMLongLatSpeedLimit(camera_long,camera_lat) )


def LongLatFromTFLid(tfl_id):
	json = JSONfromTFLCall(tfl_id)

	cam_lat = json["lat"]
	cam_long = json["lon"]

	return cam_long,cam_lat

camera_id = "01460"
camera_long,camera_lat = LongLatFromTFLid(camera_id)

print(OSMLongLatSpeedLimit(camera_long,camera_lat))