import facebook
import requests
import pdb
import time
import json

from facebook_api_settings import * # holds access token

sleep_time = 5
save_dir = 'data2/'

#####################
# EXTRACT GROUP IDS #
#####################
file_dir = save_dir + 'groups_id.txt'
file_h = open(file_dir, 'r')
groups_id_list = list()
for line in file_h:
    gid = line[:-1] # remove the '\n'
    groups_id_list.append(gid)
file_h.close()
#####################

message_page = open(save_dir+'all_posts.txt', 'w') # stores posts for all groups
total_message = 0
num_posts_wanted_per_group = 5000 

for group_id in groups_id_list:
	print 'Crawling info from: ' + group_id + '\n'
	storage_page = open(save_dir+group_id+'.txt', 'w') # stores post, username, number of likes and comments for each group
	
	graph = facebook.GraphAPI(access_token = access_token_e, version = '2.2')
	group_feed = graph.get_connections(id = group_id, connection_name = 'feed', limit = 500) # limit states how many posts per page you want
	
	page_num = 0 
	while True: 
		try:
			feeds = group_feed['data']
			for feed in feeds:
				comment_num = 0
				like_num = 0

				########
				# POST #
				########
				if feed.has_key('message'):
					message = feed['message'].encode('ascii', 'ignore')
					message = message.replace('\n', ' ')
					person = feed['from']['name'].encode('ascii', 'ignore')

					message_page.write(message + '\n\n')
					total_message += 1

					#########
					# LIKES #
					#########
					if feed.has_key('likes'):
						feed_likes = feed['likes']
						while True:
							try:
								like_num += len(feed_likes['data'])
								if feed_likes['paging'].has_key('next'):
									time.sleep(sleep_time) # facebook api can query 600 calls per 600 seconds, so I sleep the code for 1 second after each call
									feed_likes = requests.get(feed_likes['paging']['next']).json()
								else:
									break
							except KeyError:
								break
					#########

					############
					# COMMENTS #
					############
					if feed.has_key('comments'):
						feed_comments = feed['comments']
						while True:
							try:
								comment_num = len(feed_comments['data'])
								if feed_comments['paging'].has_key('next'):	
									time.sleep(sleep_time) # facebook api can query 600 calls per 600 seconds, so I sleep the code for 1 second after each call
									feed_comments = requests.get(feed_comments['paging']['next']).json()
								else:
									break
							except KeyError:
								break
					############

					post_obj = {u"user": person, u"post": message, u"likes": like_num, u"comments": comment_num}
					post_info = json.dumps(post_obj)
					storage_page.write(post_info + '\n\n')

				########
	
			print 'Page ' + str(page_num) + ' complete.\n'
			page_num += 1
			print 'Posts Crawled: ' + str(total_message) + '\n' 

			if total_message >= num_posts_wanted_per_group:
				num_posts_wanted_per_group = 0
				break

			time.sleep(sleep_time) # facebook api can query 600 calls per 600 seconds, so I sleep the code for 1 second after each call
			group_feed = requests.get(group_feed['paging']['next']).json()
		except KeyError:
			break

	storage_page.close()
	
message_page.close()

print 'Done\n'