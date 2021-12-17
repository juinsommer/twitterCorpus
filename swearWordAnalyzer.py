# Import the Twython class 
from typing import Sequence
from twython import Twython 
import json

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

#read in user word to search
print("Search keyword: ")
userIn = input()

# Create our query
query = {'q': userIn,
        'result_type': 'recent',  # other options 'mixed'
        'count': 100,   # max 100
        }
import pandas as pd
# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])
# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)

pd.set_option('display.max_columns', None)
#pd.set_option('show_dimensions', False)
pd.set_option('display.width', None)
pd.set_option('styler.sparse.index', True)
pd.set_option('styler.sparse.columns', True)


contains1 = df.text.str.contains(userIn, case = False).sum()
print("Number of occurrences: ", contains1)
print("Number of tweets: ", df.user.size)
print(df, '\n')

#writes txt file of search output
df.to_csv('searchOutput.txt', header = None, index = None, sep ='\n', mode = 'w', compression = 'infer', columns = None)

entry = ' '
while entry != 'q' :
    entry = int(input("Search by Entry: "))
    search = df[entry : entry+1]
    pd.set_option('display.latex.multirow', True)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    print(search, '\n')
