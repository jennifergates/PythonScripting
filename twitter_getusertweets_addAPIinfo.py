# Links used:
# How to get API and install Twitter library:
# http://socialmedia-class.org/twittertutorial.html
# How to loop to get more tweets than rate limit allows
# https://dev.twitter.com/rest/reference/get/statuses/user_timeline

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API
#### !!!! Must add your own. see link above on how to get

ACCESS_TOKEN = 'YourAccessToken'
ACCESS_SECRET = 'YourAccessSecret'
CONSUMER_KEY = 'YourConsumerKey'
CONSUMER_SECRET = 'YourConsumerSecret'

screenname = "jgsecure"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth)

tweets_file = twitter.statuses.user_timeline(screen_name=screenname,count=3200,exclude_replies=1,include_rts=0)
#print tweets_file
for tweet in tweets_file:
    #print line
   if 'text' in tweet: # only messages contains 'text' field is a tweet
        #print tweet['id'] # This is the tweet's id
        print tweet['text'] # content of the tweet

latest = 1;
# get last tweet to start next pull from
tweet_id = tweets_file[-1]['id'] - 1

while tweet_id > latest:
    tweets_file = twitter.statuses.user_timeline(screen_name=screenname,max_id=tweet_id,count=3200,exclude_replies=1,include_rts=0)
    for tweet in tweets_file:
        if 'text' in tweet: # only messages contains 'text' field is a tweet
            print tweet['text'] # content of the tweet
    try:
        tweet_id = tweets_file[-1]['id'] - 1
    except:
        latest = 10000000000000000000000000000000000
