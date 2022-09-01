# importing required library 
from bleach import clean
import mysql.connector 
import nltk
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords #imports stopwords from nltk
from nltk.classify import NaiveBayesClassifier
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from textblob import TextBlob
import translators as ts

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
    
# connecting to the database 
dataBase = mysql.connector.connect(
                     host = "localhost",
                     user = "root",
                     passwd = "root",
                     database = "sentiment-analyzer",
                     port = 8889 ) 
    
# preparing a cursor object 
cursorObject = dataBase.cursor()

def get_data_latih():
    # selecting query
    query = "SELECT * FROM t_data_tweets a"
    query += " LEFT OUTER JOIN `t_data_uji` u ON a.`tweet_id` = u.`tweet_id`"
    query += " WHERE"
    query += " (u.`tweet_id` IS NULL)"
    
    cursorObject.execute(query)
    
    myresult = cursorObject.fetchall()

    return myresult

def get_data_uji():
    # selecting query
    query = "SELECT * FROM t_data_uji"
    cursorObject.execute(query)
    myresult = cursorObject.fetchall()

    return myresult

def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("indonesian")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict
  
def analyze_tweets():
    train_arr_neg_words = []
    train_arr_pos_words = []
    train_arr_neutral_words = []
    test_arr_neg_words = []
    test_arr_pos_words = []
    test_arr_neutral_words = []
    arr_test_words = []
    arr_train_words = []

    data_train = get_data_latih()
    for x in data_train:
        clean_tweet = x[3]
        sentiment   = x[5]

        stemmed_tweet = stemmer.stem(clean_tweet)

        if (sentiment == 'negative') :
            neg_words = word_tokenize(stemmed_tweet)
            train_arr_neg_words.append((create_word_features(neg_words),"negative"))
        elif (sentiment == 'positive') :
            pos_words = word_tokenize(stemmed_tweet)
            train_arr_pos_words.append((create_word_features(pos_words),"positive"))
        else :
            neutral_words = word_tokenize(stemmed_tweet)
            train_arr_neutral_words.append((create_word_features(neutral_words),"neutral"))

    arr_train_words = train_arr_neg_words + train_arr_pos_words + train_arr_neutral_words

    data_test = get_data_uji()
    for x in data_test:
        clean_tweet = x[1]
        sentiment   = x[2]

        stemmed_tweet = stemmer.stem(clean_tweet)
        
        if (sentiment == 'negative') :
            neg_words = word_tokenize(stemmed_tweet)
            test_arr_neg_words.append((create_word_features(neg_words),"negative"))
        elif (sentiment == 'positive') :
            pos_words = word_tokenize(stemmed_tweet)
            test_arr_pos_words.append((create_word_features(pos_words),"positive"))
        else :
            neutral_words = word_tokenize(stemmed_tweet)
            test_arr_neutral_words.append((create_word_features(neutral_words),"neutral"))

    arr_test_words = test_arr_neg_words + test_arr_pos_words + test_arr_neutral_words

    classifier = NaiveBayesClassifier.train(arr_train_words)

    for x in data_test:
        tweet_id = x[0]
        clean_tweet = x[1]

        stemmed_tweet = stemmer.stem(clean_tweet)
        
        # start textblob sentiment result
        tweet_translated = ts.google(stemmed_tweet)
        
        analysis = TextBlob(tweet_translated)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0:
            sentiment_textblob = 'positive'
        elif polarity < 0:
            sentiment_textblob = 'negative'
        else:
            sentiment_textblob = 'neutral'

        # start naivebayes sentiment result
        words = word_tokenize(stemmed_tweet)
        words = create_word_features(words)
        sentiment_result = classifier.classify(words)

        # updating data uji
        query = "UPDATE `t_data_uji` SET naive_bayes_analysis = '" + sentiment_result + "', textblob_analysis = '" + sentiment_textblob +"' WHERE tweet_id = %s"
        cursorObject.execute(query, (tweet_id,))

    # delete data
    # query = "DELETE FROM t_data"
    # cursorObject.execute(query)

    # insert data
    accuracy = nltk.classify.util.accuracy(classifier, arr_test_words)
    query = "UPDATE t_data SET accuracy = (%s)"
    cursorObject.execute(query, (accuracy,))


    # disconnecting from server
    dataBase.commit()

    return ""
