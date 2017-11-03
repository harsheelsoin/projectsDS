#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 02:18:43 2017

@author: harsheelsoin
"""

import os
#change working directory to path where HW3 folder downloaded as per your system
os.chdir('/Users/harsheelsoin/Downloads/Projects in Data Science/Homeworks/HW3')

from crawler import *
from classifier import *
from predictor import *
import tweepy  
from pymongo import MongoClient
from textwrap import TextWrapper
from tweepy.utils import import_simplejson
json = import_simplejson()

#Required to use your own twitter application credentials
auth1 = tweepy.auth.OAuthHandler('RaS3csW5CPQB4sPKrDqv6k9Vi','k7kSKTl7N0O6lNUHxWQZCvVpdq9qvUIbpCDs9dvnSvFGHWXVOj')  
auth1.set_access_token('128463276-ExmhyHgTnc6sIJRXiCgZHNbmoG6DkDPr2lgZZZVW','yTD8h8NHTgTwvHCBf9bql1eIyEVJtEs2PMjh0W6WtyrdH')  
api = tweepy.API(auth1)

topics = ["politics", "astronomy", "medical", "music", "sports"]

current_directory = os.getcwd()
#dir_path = os.path.dirname(os.path.realpath('__file__'))

#creating a crawler object to generate training data for classification
crawlerObj = theCrawler()

#creating list of urls for each category
allIndices = crawlerObj.theIndexer(topics,current_directory)
#scraping text (training data) from urls html (meeting required criteria) and storing in text files in respective category directories
allDocumentsWordCount = crawlerObj.dataGenerator(allIndices,topics,current_directory)
#allDocumentsWordCount contains the number of words (>50) contained in each txt file in each classification category

mainPath = current_directory+'/'
theDataPath = os.path.abspath("theData")
theDataPath+="/"

classes = os.walk(theDataPath).next()[1]
theLabels = classes 

finalWords = list()
theDocs = list()

#starting the classification once the training data is ready
classifyObj = theClassifier()

#preparing text from all training txt files in respective scraped-data sub-directories for model
for word in classes:
    cnt = 0
    for file in os.listdir(theDataPath+word):
        if file.endswith('.txt'):
            try:
                f = open(theDataPath + word + "/" + file, "r")
                lines = f.readlines()
                lines = [text.strip() for text in lines]
                lines = " ".join(lines)
                finalWords.append(classifyObj.genCorpus(lines))
                theDocs.append(classifyObj.textToNum(theLabels,word) +"_" + str(cnt))
                cnt = cnt +  1
            except:
                pass

tdm = classifyObj.vec(finalWords,1000,1,1,theDocs)

reducedTDM = classifyObj.pca(tdm,0.95,theDocs)

fullIndex = reducedTDM.index.values
fullIndex = [int(word.split("_")[0]) for word in fullIndex]

#Training a RF model and outputing to a file for future use in predicting classes
classifyObj.modelTrain(['RF'],reducedTDM,fullIndex,10,mainPath)

#sample text classification, classify arbitary text into any of the five classes
tempText = "politics Trump democracy policy economics election defeat elect musical sporty medicine stars sun moon Taylor Swift Eminem galaxy golf quarterback cricket football"
predictObj = thePredictor()
testText=list()
testText.append(predictObj.genCorpus(tempText))
thePredictedClass = predictObj.predictClass(mainPath,classes,testText)

#setting up mongodb and collections for twitter data post classification
mongo = MongoClient('localhost', 27017)
mongo_db = mongo['twitterDBs']
mongo_collection = mongo_db['theData']

#Tweet StreamListener class for continous tweet streaming, classification and storage into mongodb
class StreamListener(tweepy.StreamListener):  
    status_wrapper = TextWrapper(width=140, initial_indent='', subsequent_indent='')
    def on_status(self, status): 
        tempA = self.status_wrapper.fill(status.text)
        tempB = status.retweeted 
        tempC = status.user.lang 
        tempD = status.geo
        print tempD
        if ((("en" in tempC) and (tempB is False)) and (not("RT") in tempA[:2]) and (((("http" or "www") in tempA) and ((' ') in tempA)) or (not("http" or "www") in tempA))):
            try:     
                print(self.status_wrapper.fill(status.text))
                tempText = self.status_wrapper.fill(status.text)
                theText = list()
                theText.append(predictObj.genCorpus(tempText))
                predictedClass = predictObj.predictClass(mainPath,classes,theText)
                mongo_collection.insert({
                'followers': status.user.followers_count,
                'screen_name': status.author.screen_name,
                'friends_count': status.user.friends_count,
                'created_at': status.created_at,
                'message_id': status.id,
                'location': status.user.location,
                'body': self.status_wrapper.fill(status.text),
                'topic': predictedClass
                })
            except Exception, (e):  
                print("HERE")          
                pass
#creating StreamListener object
l = StreamListener()  
streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000)

#Tweet search terms for continous streaming   
setTerms = ["potus","moon and the sun","pharmacy","drake", "quarterback"]
streamer.filter(None,setTerms)

#Please stop code execution when obtained required number of classified tweets in mongodb