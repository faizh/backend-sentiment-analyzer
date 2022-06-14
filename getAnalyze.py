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


# In[2]:


def connect_to_twitter():
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHdHdgEAAAAAgPDw6GUk0r2%2BWXfjbchVb9XBYZk%3Dm17s8NVA1f9b5rpqANFKsb8PUBXA4ERcAUKv65nhZE5Wxx56wA'
    return {"Authorization" : "Bearer " + bearer_token}


# In[5]:


headers = connect_to_twitter()


# In[6]:


def make_request(headers):
    url = "https://api.twitter.com/2/tweets/search/recent?"
    max_result = "max_results=100"
    #query = "query=conversation_id:1535888836898607104 OR url:1536230662457307137"
    query = "query=indihome -is:retweet"
    #query = "query=from:twitterdev -is:reply -is:retweet"
    params = max_result + "&" + query
    return requests.request("GET", url, params=params, headers=headers).json()


# In[18]:


def get_tweets_data():

    tweets = make_request(headers)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []

    for tweet in tweets['data']:
        original_tweet = tweet['text']
        tweet['text'] = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet['text']).split())
        analysis = TextBlob(tweet['text'])
        try:
            an = analysis.translate(from_lang='id', to='en')        
        except:
            continue
        
        polarity = an.sentiment.polarity
        
        if polarity > 0:
            positive += 1
        elif polarity < 0:
            negative += 1
        else:
            neutral += 1
        
        tweet_properties = {
            'tweet_id' : tweet['id'],
            'original_tweet' : original_tweet,
            'polarity' : polarity
        }
        
        tweet_list.append(tweet_properties)

    return json.dumps(tweet_list)
    # return "success return"
