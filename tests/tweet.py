#!/usr/bin/env python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python tweet.py start

#standard python libs
import os
import sys
from time import sleep
import random

#third party libs
from twitter import *


TOCTOC_PATH = '/usr/share/toctoc/'
CONSUMER_K3Y = 'WklI49k0O3Z2ZuMKgOQaBg'
CONSUMER_S3CR3T = 'E27Dt7NnTYVIswqsz4o5r8U1o2VJ0ekbF7vOC1iTlg'
MY_TWITTER_CREDS = TOCTOC_PATH + '.toctoc_credentials'

#authenticate
if not os.path.exists(MY_TWITTER_CREDS):
      oauth_dance("toctoc", CONSUMER_K3Y, CONSUMER_S3CR3T, MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_K3Y, CONSUMER_S3CR3T))

#tweet
randomstatus = "Hello @toctocParis, I'm going through the toctoc tutorial: http://soixantecircuits.github.com/toctoc"
twitter.statuses.update(status=randomstatus)
