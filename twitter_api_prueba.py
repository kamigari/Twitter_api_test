#! /usr/bin/python

import twitter, json
from tokens import OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET

twitter_api = statuses = lang = q = None

def set_oauth():
    global twitter_api
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

def get_tweets():
    '''Use the '''
    global statuses, q
    print('Introduzca un hashtag para buscar en twitter:')
    hastag = input('#')
    q = '#' + hastag

    count = 100
    
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses'] 

    for _ in range(count):
        print ("Length of statuses", len(statuses))
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError: # No more results when next_results doesn't exist
            break
        
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

def put_into_txt():
    '''Just put the output in a txt file'''
    with open('hashtag.txt', 'w') as outfile:
        json.dump(statuses, outfile, indent = 4)
        #print (json.dumps(statuses[0], indent=1))

def get_languajes():
    '''Setting up the dict with the values of the languajes'''
    global statuses, lang
    lang = {}
    for _ in range(len(statuses)):
        if(statuses[_]['user']['lang'] in lang):
            lang[statuses[_]['user']['lang']] += 1
        else:
            lang[statuses[_]['user']['lang']] = 1
    print(lang)

def get_histogram(dict):
    '''Get a histogram from the values of the dict'''
    import pylab as pl
    import numpy as np
    global q
    X = np.arange(len(dict))
    pl.bar(X, dict.values(), align='center', width=0.5)
    pl.xticks(X, dict.keys())
    ymax = max(dict.values()) + 1
    pl.ylim(0, ymax)
    pl.savefig('histogram_languajes_'+ q +'.png')
    pl.show()

if __name__ == "__main__":

    set_oauth()
    get_tweets()
    put_into_txt()
    get_languajes()
    get_histogram(lang)
