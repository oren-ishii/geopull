#!/usr/bin/env python2
import pytumblr
import shutil, requests
import time, sys, os

src = []
urls = []
collection = []
optimal_factor = None

#Tumblr api is convenient to use, so go get your key and oauth token.
consumer_key = None
consumer_secret = None
oauth_token = None
oauth_secret = None

client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    oauth_token,
    oauth_secret,
)
#Tumblr API is kinda nice, but it limits queries to 20 posts at a time.
#It also doesn't provide a real nice way of knowing when you've hit the
#end of the posts, and instead just gives you back the same last couple 
#posts. This just queries the profile's total post count, and pulls 20 
#at a time until there are less than 20 left, gets the difference, and
#makes one final query with size equal to that difference to get the 
#exact post count. 
def getPosts(client, user):
	offset = 0
	done = False
	optimal_factor = 20
	try:
		post_count = client.posts(user)['total_posts']
		print "[+] Total posts: " + str(post_count)
	except KeyError:
		print "[!] Profile not found."
		sys.exit(1)
	print "[+] Crawling page for posts...\n"
	while not done:
		if offset >= post_count:
			done = True
			print "\n[+] Done getting posts."
		elif (post_count - offset) < 20:
			optimal_factor = post_count - offset
			posts = client.posts(user, limit=optimal_factor, offset=offset)
			for post in posts['posts']:
				collection.append(post)
			offset += optimal_factor
			print "[*] Crawled " + str(offset) + " posts."
		else:
			posts = client.posts(user, limit=optimal_factor, offset=offset)
			for post in posts['posts']:
				collection.append(post)
			offset += optimal_factor
			print "[*] Crawled " + str(offset) + " posts."

#If the post has photos attached, stick it in the collection
def identifyPhotoPosts():
	for x in collection:
		if 'photos' in x.keys():
			for y in x['photos']:
				if 'exif' in y.keys():
					src.append(y)
#Put the urls for the images in a collection
def processURLS():
	for x in src:
		urls.append(x['original_size']['url'])

#Follow the URLs in our collection and download each of the images
#to the working directory. 
def fetchImages(user):
	print "[+] Beginning to download images. This can take a while, be patient."
	count = 0
	if not os.path.exists('images/' + user + '/'):
		os.makedirs('images/' + user + '/')
	for url in urls:
		count += 1
		#print url
		response = requests.get(url, stream=True)
		with open('images/' + user + '/' + str(count) + '.jpg', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)

	


