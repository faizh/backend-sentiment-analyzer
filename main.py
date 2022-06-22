#!/usr/bin/env python
# coding: utf-8

# In[7]:


import flask
# from requests.api import request
from flask import request
import getAnalyze
import naiveBayesAnalysis

# In[8]:


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# In[9]:


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/getTweets', methods=['POST'])
def getTweets():
    start_date  = request.form.get('start_date')
    end_date    = request.form.get('end_date')
    return getAnalyze.get_tweets_data(start_date, end_date)

@app.route('/test', methods=['GET'])
def test():
    return getAnalyze.test()

@app.route('/analyzeNaiveBayes', methods=['GET'])
def analyzeNaiveBayes():
    return naiveBayesAnalysis.analyze_tweets()

# In[10]:

app.run(port=4996)

# In[ ]: