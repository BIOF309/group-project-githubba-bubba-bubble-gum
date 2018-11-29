import numpy as np
import pip
import tweepy
import json
import csv
import pandas as pd
consumer_key = 'kbMAphoqE5gMUJIofDwRAA8Mm'
consumer_secret = '8XiLrPhol1L6FVxHGXgQgNEh0ngvUx5xlQUXny0ZiI6Q0Uue7I'
access_key = '878766942085156865-IOJccRODzhK4JsQGHfu0s6k5geBoZMs'
access_secret = 'dlZbMrubLkzLTbnvq32htRoR4seZHrym4n2MxOwE0o0hx'

def twitter_setup():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)
    return api


extractor = twitter_setup()

tweets = extractor.user_timeline(screen_name='realDonaldTrump', count=3200)
print('Number of tweets extracted: {}.\n'.format(len(tweets)))

print('5 recent tweets:\n')

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
display(data)
for tweet in tweets[:-1]:
    print(tweet.text)
    print()
