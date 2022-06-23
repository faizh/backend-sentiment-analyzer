#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import os
from textblob import TextBlob
import re
from textblob.classifiers import NaiveBayesClassifier
import json
import translators as ts

import model

# In[2]:


def connect_to_twitter():
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHdHdgEAAAAAfeShfQ5b43jfs7zVyTTjTpecq68%3D0rbfMnF974zUZEeYpu72Y7gDSKlEULZx6LMp1KfGbgEvkkajJY'
    return {"Authorization" : "Bearer " + bearer_token}


# In[5]:


headers = connect_to_twitter()


# In[6]:


def make_request(headers, start_date, end_date):
    url = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=100"
    start_time  = "start_time=" + start_date
    end_time    = "end_time=" + end_date
    #query = "query=conversation_id:1535888836898607104 OR url:1536230662457307137"
    query = "query=indihome -is:retweet"
    #query = "query=from:twitterdev -is:reply -is:retweet"
    tweet_fields = "tweet.fields=created_at,author_id"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query + "&" + tweet_fields
    # print(params)
    return requests.request("GET", url, params=params, headers=headers).json()


# In[18]:

def test():
    analysis = TextBlob('test')
    try:
        an = analysis.translate(from_lang='id', to='en')        
    except:
        print("error")
    
    polarity = an.sentiment.polarity

    if polarity > 0:
        sentiment = 'positive'
    elif polarity < 0:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment
    

def get_tweets_data(start_date, end_date):
    # tweets = make_request(headers, start_date, end_date)
    tweets      = json.loads(model.get_conversation_from_tweet_id(start_date, end_date))
    polarity = 0
    tweet_list = []
    sentiment = ""

    for tweet in tweets:
        original_tweet = tweet['text']
        tweet['text'] = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\d+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet['text']).split())
        tweet['text'] = tweet['text'].lower()
        tweet_translated = ts.google(tweet['text'])
        
        analysis = TextBlob(tweet_translated)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0:
            sentiment = 'positive'
        elif polarity < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        tweet_properties = {
            'tweet_id' : tweet['id'],
            'author_id' : tweet['author_id'],
            'original_tweet' : original_tweet,
            'clean_tweet' : tweet['text'],
            'polarity' : polarity,
            'sentiment' : sentiment,
            'created_dtm' : tweet['created_at']
        }

        # print(tweet_properties)
        
        tweet_list.append(tweet_properties)

    return json.dumps(tweet_list)
