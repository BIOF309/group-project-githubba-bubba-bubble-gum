"""
Usage: ./tweet2.py twitter_handle threshold_value

extract twitter data from user indicated on commandline, do word frequency analysis, plot word cloud
use a threshold_value to eliminate words at lower frequencies
"""

#Import necessary packages
import tweepy, fnmatch, string
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from PIL import Image


### get in twitter environment ###
### source activate twitter ###
consumer_key = '2mQpxBXtLijGP5Ie4SIfItpS8' #API Key
consumer_secret = 'Qthv4EmSXuHdFKGx7QP6vtD4OTUjEdkZGaPEHdLvtiMNp9fyIy' #API Secret
access_key = '878766942085156865-tady67zJiuix9dhC8rhEeO4x899ZCoY' #Access Token
access_secret = 'cQHe2ZA0MqTjh1K9Fq3OekbCIUbFMNf4WVOby3tZsP6Ga' #Access Token Secret



def get_all_tweets(screen_name):
    """Ping a Twitter account and extract ~3200 tweets. Can only extract 200 tweets at a time.
    Credit to https://gist.github.com/yanofsky/5436496 but change python2 things to python3
    for parts of function."""

    # Twitter only allows access to a users most recent ~3240 tweets with this method
    # at Trump's tweet rate, that gets us approx. 11 months of tweets
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets into alltweets list
    alltweets.extend(new_tweets)

    # save the id of the next tweet that wasn't originally pulled
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsequent requests use the max_id paramater to prevent duplicates
        # and pull the next group of tweets
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets into alltweets list
        alltweets.extend(new_tweets)

        # save the id of the next tweet that wasn't originally pulled
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a utf-8 encoded, then decoded list of lists
    outtweets = [[tweet.full_text.encode("utf-8")] for tweet in alltweets]
    outtweets = [[tweet.decode("utf-8", "ignore")] for sublist in outtweets for tweet in sublist]


    return outtweets

### pass in the username of the account you want to extract the tweets from ###
user_name = 'realDonaldTrump' #can input a different twitter handle here to analyze
DJT = get_all_tweets(user_name) # run the function and store


### write the data into a txt file ###
### credit https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python ###
with open('%s_tweets.txt' % user_name, 'w', encoding="windows-1252", errors="ignore") as f:
    for item in DJT:
        for j in item:
            f.write("%s\n" % item)


### read the txt file onto one line ###
def read_file(filename):
    with open(filename, 'r', encoding="cp1252", errors='ignore') as f:
        return f.read()

read_file('realDonaldTrump_Tweets.txt')

### separate each tweet ###
### Thanks for the help Martin! ###
lines = [line for line in read_file('%s_tweets.txt' % user_name).split('\n') if line is not '']
 print(lines[-1])


### split tweets into 2 lists: retweets and orig_tweets ###
retweets = [] #can ignore this list, since we are not analyzing retweets
orig_tweets = []
for tweet in lines:
    #print(tweet)
    if "RT" in tweet:
        retweets.append(tweet)
    else:
        orig_tweets.append(tweet)

# print(orig_tweets)
# print(retweets)
 print(len(orig_tweets))
 print(len(retweets))

### from orig_tweets, exclude words that contain numbers, @, or url's into word_list ###
unwanted_word_list = []
word_list = []
for tweet in orig_tweets:
    #print(tweet)
    fields = tweet.strip("\r\n").split() #splits strings in orig_tweets into lists of strings
    #print(fields)                       #where each word is it's own string
    for word in fields:
        #print(word)
        ### Exclude meaningless words, twitter handles, numbers, and URLs ###
        exclusions = ["*https://*", "*@*", "*1*", "*2*", "*3*", "*4*",
        "*5*", "*6*", "*7*", "*8*", "*9*", "*0*", "the", "a", "and",
        "to", "on", "is", "in", "of", "for", "with", "that","be",
        "will", "it", "as", "was", "at", "are", "this", "from","has",
        "have", "so","who","his","being","an","about","he","their",
        "which","would","get","there","when","going","you"]
        if any(fnmatch.fnmatch(word, exclusion) for exclusion in exclusions):
            unwanted_word_list.append(word)
        else:
            # remove punctuation from word strings
            translator = str.maketrans('', '', string.punctuation)
            word = word.translate(translator)
            word_list.append(word.lower())


### for some reason there were still some words we tried to exclude, so we ran this again ###
### and it excluded the rest ###
unwanted_word_list2 = []
word_list2 = []
for word in word_list:
    exclusions = ["the", "a", "and", "to", "on", "is", "in", "of", "for", "with",
                  "that", "be", "will", "it", "as", "was", "at", "are", "this",
                  "from", "has", "have", "so", "who", "his", "being", "an", "about",
                  "he", "their","which", "would", "get", "there", "when", "going",
                  "you","they","by","just","amp","","been","or","than","if","had"]
    if any(fnmatch.fnmatch(word, exclusion) for exclusion in exclusions):
        unwanted_word_list2.append(word)
        # continue # if you want to skip these tweets
    else:
        word_list2.append(word)

### get word frequency from word_list and put into dictionary ###
counts = Counter(word_list2) # count word frequency and put into dictionary
print(counts)
threshold_value = 50
threshold_counts = {} # new dictionary with only words above threshold value
for key, value in counts.items():
    if value > threshold_value:
        threshold_counts[key] = value
print(threshold_counts)
print(len(threshold_counts))

### wordcloud using threshold_counts ###
### credit https://stackoverflow.com/questions/43043437/ ###
### wordcloud-python-with-generate-from-frequencies?rq=1 for help###
wordcloud = WordCloud(width=1800, height=1000, max_words=500,relative_scaling=1,
normalize_plurals=True).generate_from_frequencies(threshold_counts)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
plt.savefig("tweet_word_cloud_{}.png".format(user_name))
plt.close()

















