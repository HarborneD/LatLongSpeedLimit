import urllib.request
import xmltodict
import xml.etree.ElementTree as ET

import json

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

def OSMLongLatSpeedLimit(cam_long,cam_lat,start_box_size = 0.00000002, step_dist =  0.0001,attempt_count = 10 ):
	
	ways = []

	step = start_box_size
	while ((len(ways) != 1) and attempt_count > 0 and step > 0):
		box_long = str(float(cam_long) - step)

		box_lat = str(float(cam_lat) - step)

		box_long2 = str(float(cam_long) + step)

		box_lat2 = str(float(cam_lat) + step)

		tree = XMLfromOSMSpeedCall(box_long,box_lat,box_long2,box_lat2)

		road_speeds = {}

		unknown_counter = 0

		ways = tree.getroot().findall('way')

		print(len(ways))
		if(len(ways) != 1):
			if(len(ways) > 1):
				step -= step_dist
			else:
				step += step_dist

		attempt_count -= 1

	for way in ways:
		way_tags = way.findall('tag')
		for tag in way_tags:
			pass
			#print(tag.attrib.get('k'),tag.attrib.get('v'))

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

def LongLatFromTFLid(tfl_id):
	json = JSONfromTFLCall(tfl_id)

	cam_lat = json["lat"]
	cam_long = json["lon"]

	return cam_long,cam_lat

if(__name__ == "__main__"):
	camera_id = "01460"
	camera_long,camera_lat = LongLatFromTFLid(camera_id)

	print(OSMLongLatSpeedLimit(camera_long,camera_lat))