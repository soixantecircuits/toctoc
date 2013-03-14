# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python cuicui.py start

#standard python libs
import logging
import os
import sys
from time import sleep
from urllib2 import HTTPError

#third party libs
from daemon import Daemon
from twitter import *

TOCTOC_PATH = '/usr/share/toctoc/'
CONSUMER_K3Y = 'WklI49k0O3Z2ZuMKgOQaBg'
CONSUMER_S3CR3T = 'E27Dt7NnTYVIswqsz4o5r8U1o2VJ0ekbF7vOC1iTlg'
MY_TWITTER_CREDS = TOCTOC_PATH + '.toctoc_credentials'
if not os.path.exists(MY_TWITTER_CREDS):
  oauth_dance("toctoc", CONSUMER_K3Y, CONSUMER_S3CR3T, MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

twitter_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, CONSUMER_K3Y, CONSUMER_S3CR3T))

iterator = twitter_stream.statuses.filter(track="#toctoc", block=False)
while True:
   if iterator is not None:
	for tweet in iterator:
	  if ('Soixanteci' in map(lambda x:x['screen_name'], tweet['entities']['user_mentions'])) or (tweet['user']['screen_name'] =='Soixanteci'):
            print tweet['user']['name'] + "(@" + tweet['user']['screen_name'] +"):\t" + tweet['text']
	    os.system('mpg321 ' + TOCTOC_PATH + 'dong.mp3 &')
   sleep(0.1)
          
