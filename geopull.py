#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import PIL, os, sys
from tumblecrawl import *
from PIL import Image
from PIL import ExifTags
from geopy.geocoders import Nominatim
banner = '''
                              _ _
  __ _  ___  ___  _ __  _   _| | |
 / _` |/ _ \/ _ \| '_ \| | | | | |
| (_| |  __/ (_) | |_) | |_| | | |
 \__, |\___|\___/| .__/ \__,_|_|_|
 |___/           |_|              
                   
 By: O-Ren Ishii
 
'''

#For convenience
g = 'GPSInfo'
exif_data = None
#Images path
path = None
files = None

#Create a list of images in the working directory
def getDirListing():
	global files
	files = os.listdir(path)

def getInfo(exif):
	lat = str(exif[g].get(1)) , str(exif[g].get(2)[0][0]) , str(exif[g].get(2)[1][0]) , str(exif[g].get(2)[2][0])[:-3] + "." + str(exif[g].get(2)[2][0])[-3:]
	lon = str(exif[g].get(3))[0] , str(exif[g].get(4)[0][0]) , str(exif[g].get(4)[1][0]) ,  str(exif[g].get(4)[2][0])[:-3] + "." + str(exif[g].get(4)[2][0])[-3:]
	return lat, lon

#Perform the geography lookup using Nominatim (https://nominatim.openstreetmap.org/)
def doLookup(latitude, longitude):
	geolocator = Nominatim()
	try:
		location = geolocator.reverse(str(latitude) + ", " + str(longitude), exactly_one=True)
		print location.address
		print
	except:
		sleep(2)
		doLookup(latitude, longitude)

#Process the old degrees, minutes, seconds format into standard (positive/negative) degrees format
def convertToDecimalDegrees(coordinate):
	nsew = coordinate[0]
	deg = coordinate[1]
	min = coordinate[2]
	sec = coordinate[3]
	decimal = 0.0
	modifier = 1;
	if (nsew == 'N' or nsew == 'E'):
		pass
	elif (nsew == 'S' or nsew == 'W'):
		modifier *= -1
	decimal = float(deg) + float(min)/60 + float(sec)/3600
	return decimal*modifier

#This just prints out the fancied and fixed coords, nothing special
def printFormatted(latitude, longitude):
	print "[" + str(latitude) , "," , str(longitude) + "]"

#Starting point. This grabs the info from the sorted collection, converts the coordinate format to the one we need,
#and performs/prints the geography lookup info. Not too complicated.
def main():
	user = sys.argv[1]
	global path
	path = 'images/' + sys.argv[1] + "/"
	getPosts(client, user)
	identifyPhotoPosts()
	processURLS()
	fetchImages(user)
	getDirListing()
	print "[*] Here's what we recovered:\n"
	for filename in files:
		with PIL.Image.open(path + filename) as img:
			try:
				exif_data = img._getexif()
				sorted = {
				PIL.ExifTags.TAGS[k]: v
   				for k, v in img._getexif().items()
	   			if k in PIL.ExifTags.TAGS
				}
				coordinates = getInfo(sorted)
				if not coordinates:
					return
				else:
					latitude = convertToDecimalDegrees(coordinates[0])
					longitude = convertToDecimalDegrees(coordinates[1])
					print path + filename
					printFormatted(latitude, longitude)
					doLookup(latitude, longitude)
			except:
				pass
		
	print "[*] Done!"

#Hurr durrr
if __name__ == '__main__':
	print banner
	if len(sys.argv) < 2:
		print "Usage: %s [username]" % sys.argv[0]
	else:
		try:
			main()
		except KeyboardInterrupt:
			print "\n[!] Caught Ctrl+C, shutting down."
