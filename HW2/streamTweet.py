import tweepy  
from pymongo import MongoClient
from textwrap import TextWrapper
from tweepy.utils import import_simplejson
from predictor import *    #importing 'thePredictor' class from predictor.py
json = import_simplejson()

#Required to use your own twitter application credentials
auth1 = tweepy.auth.OAuthHandler('RaS3csW5CPQB4sPKrDqv6k9Vi','k7kSKTl7N0O6lNUHxWQZCvVpdq9qvUIbpCDs9dvnSvFGHWXVOj')  
auth1.set_access_token('128463276-ExmhyHgTnc6sIJRXiCgZHNbmoG6DkDPr2lgZZZVW','yTD8h8NHTgTwvHCBf9bql1eIyEVJtEs2PMjh0W6WtyrdH')  
api = tweepy.API(auth1)

mongo = MongoClient('localhost', 27017)
mongo_db = mongo['twitterDBs']
mongo_collection = mongo_db['theData']

#Input directory path to training data
thePath = os.path.abspath("classify")
thePath+="/"

#Path to script's working directory
directoryPath = os.path.dirname(os.path.abspath(__file__))
directoryPath+="/"

#Obtaining class names from "classify" directory
classes = os.walk(thePath).next()[1]

#Creating a class predictor object
predictObj = thePredictor()

class StreamListener(tweepy.StreamListener):  
    status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')    
    def __init__(self, api=None):
        super(StreamListener, self).__init__()
        self.num_tweets = 0                 #adding tweet counter within 'StreamListener' class
    def on_status(self, status): 
        tempA = self.status_wrapper.fill(status.text)
        tempB = status.retweeted 
        tempC = status.user.lang 
        tempD = status.geo
        print tempD
        if ((("en" in tempC) and (tempB is False)) and (not("RT") in tempA[:2]) and (((("http" or "www") in tempA) and ((' ') in tempA)) or (not("http" or "www") in tempA))):
            try:     
                self.num_tweets += 1         #maintaining a tweet counter
                if self.num_tweets <= 100:   #ensuring only 100 entries in mongo DB
                    print(self.status_wrapper.fill(status.text))  #printing of tweets also stops after 100 tweets that meet criteria
                    tempText = self.status_wrapper.fill(status.text)
                    theText = list()
                    theText.append(predictObj.genCorpus(tempText))
                    predictedClass = predictObj.predictClass(directoryPath,classes,theText)
                    mongo_collection.insert({
                    'body': self.status_wrapper.fill(status.text),
                    'topic': predictedClass, 
                    'followers': status.user.followers_count,
                    'screen_name': status.author.screen_name,
                    'friends_count': status.user.friends_count,
                    'created_at': status.created_at,
                    'message_id': status.id,
                    'location': status.user.location
                    })
            except Exception, (e):  
                print("HERE")          
                pass

l = StreamListener()  
streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)   
setTerms = ["fishing","hiking","machine learning","mathematics"]
streamer.filter(None,setTerms)   