import requests
import json

indihomecare_user_id = 765035200896118789

def connect_to_twitter():
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHdHdgEAAAAAfeShfQ5b43jfs7zVyTTjTpecq68%3D0rbfMnF974zUZEeYpu72Y7gDSKlEULZx6LMp1KfGbgEvkkajJY'
    return {"Authorization" : "Bearer " + bearer_token}

headers = connect_to_twitter()

def get_user_id_from_username():
    url = "https://api.twitter.com/2/users/by/username/IndiHomeCare"
    response = requests.request("GET", url, headers=headers).json()

    return response

def get_tweets_from_id(start_date, end_date):
    url         = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=100"
    start_time  = "start_time=" + start_date
    end_time    = "end_time=" + end_date
    query       = "query=from:IndiHomeCare -is:retweet -is:reply"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query
    response_tweet = requests.request("GET", url, params=params, headers=headers).json()
    
    return response_tweet

def get_tweet_to_id():
    url         = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=100"
    start_time  = "start_time=2022-06-23T00:00:00Z" 
    end_time    = "end_time=2022-06-24T00:00:00Z"
    query       = "query=to:IndiHomeCare -is:retweet"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query
    response_tweet = requests.request("GET", url, params=params, headers=headers).json()
    
    return response_tweet

def query_get_conversation_by_tweet_id(tweet_id, start_date, end_date):
    url         = "https://api.twitter.com/2/tweets/search/recent?"
    max_result  = "max_results=100"
    start_time  = "start_time=" + start_date
    end_time    = "end_time=" + end_date
    query       = "query= -is:retweet conversation_id:" + str(tweet_id) + " -from:" + str(indihomecare_user_id)
    tweet_fields = "tweet.fields=created_at,author_id"
    params = start_time + "&" + end_time + "&" + max_result + "&" + query + "&" + tweet_fields
    response_tweet = requests.request("GET", url, params=params, headers=headers).json()
    
    return response_tweet

def get_tweet_id_from_tweets_created(start_date, end_date):
    tweets_created = get_tweets_from_id(start_date, end_date)
    tweet_id = []
    for tweet in tweets_created['data']:
        tweet_id.append(tweet['id'])

    return tweet_id

def get_conversation_from_tweet_id(start_date, end_date):
    tweets_id = get_tweet_id_from_tweets_created(start_date, end_date)
    tweet_details_arr = []
    for tweet_id in tweets_id:
        tweet_details = query_get_conversation_by_tweet_id(tweet_id, start_date, end_date)
        for tweet_detail in tweet_details['data']:
            tweet_details_arr.append(tweet_detail)

    
    return json.dumps(tweet_details_arr)