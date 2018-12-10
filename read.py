def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

read_file('realDonaldTrump_tweets.txt')
lines = [line for line in read_file('realDonaldTrump_Tweets.txt').split('\n') if line is not '']

lines = [i[2:] for i in lines]
lines[5]
