#!/usr/bin/env python
# coding: utf-8

# In[7]:


import flask
import getAnalyze


# In[8]:


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# In[9]:


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/getTweets', methods=['GET'])
def getTweets():
    return getAnalyze.get_tweets_data()

# In[10]:

app.run(port=4996)

# In[ ]: