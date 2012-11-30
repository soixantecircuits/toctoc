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

class App(Daemon):
           
    def run(self):

        while True:
          try:
            TOCTOC_PATH = '/usr/share/cuicui/'
            CONSUMER_KEY = 'T4GFkDf0b6TT3YrXribSA'
            CONSUMER_SECRET = 'U8IaRjhUTshCBMQfanLV3KhIpEJsD1kBaejYwBNaB1A'
            MY_TWITTER_CREDS = TOCTOC_PATH + '.ringthebell_credentials'
            logger.debug("TWITTER CREDS PATH: " + MY_TWITTER_CREDS)
            if not os.path.exists(MY_TWITTER_CREDS):
                  oauth_dance("ringthebell", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

            oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

            twitter_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
            logger.info('Twitter OAuth successful')

            iterator = twitter_stream.statuses.filter(track="#toctoc", block=False)
            logger.info('Twitter stream connected')
            
            while self.daemon_alive:
              if iterator is not None:
                for tweet in iterator:
                  if (tweet['in_reply_to_user_id_str'] == '59809818') or (tweet['user']['id_str'] =='59809818'):
                    logger.info(tweet['user']['name'] + "(@" + tweet['user']['screen_name'] +"):\t" + tweet['text'])
                    os.system('mpg321 ' + TOCTOC_PATH + 'dong.mp3 &')
              sleep(0.1)
            logger.info('Process killed')
          except TwitterHTTPError as e:
            logger.error(e)
          except URLError as e:
            logger.error(e)
          except HTTPError as e:
            logger.error(e)
          except EOFError as e:
            logger.error(e)
          except KeyError as e:
            logger.error(e)
          except:
            logger.error("Unexpected error:")
            logger.error(sys.exc_info()[0])
            raise

              #Main code goes here ...
              #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
              #logger.debug("Debug message")
              #logger.info("Info message")
              #logger.warn("Warning message")
              #logger.error("Error message")
              #time.sleep(10)

if __name__ == "__main__":
  #daemon = App('/var/run/cuicui.pid')
  daemon = App('/tmp/cuicui.pid')

  logger = logging.getLogger("CuicuiLog")
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  handler = logging.FileHandler("/var/log/toctoc/cuicui.log")
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      logger.info('start')
      daemon.start()
    elif 'stop' == sys.argv[1]:
      logger.info('stop')
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      logger.info('restart')
      daemon.restart()
    else:
      print "usage: %s start|stop|restart" % sys.argv[0]
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)

