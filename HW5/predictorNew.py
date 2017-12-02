# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.externals import joblib
import nltk
from nltk.corpus import stopwords
import re
import os
from os.path import basename
import operator
from sklearn import preprocessing

class thePredictor(object):

    def genCorpus(self,theText):
        #set dictionaries
        stopWords = set(stopwords.words('english'))
        theStemmer = nltk.stem.porter.PorterStemmer() #Martin Porters celebrated stemming algorithm
        
        #pre-processing
        theText = theText.split()
        tokens = [token.lower() for token in theText] #ensure everything is lower case
        tokens = [re.sub(r'[^a-zA-Z0-9]+', ' ',token) for token in tokens] #remove special characters but leave word in tact
        tokens = [token for token in tokens if token.lower().isalpha()] #ensure everything is a letter
        tokens = [word for word in tokens if word not in stopWords] #rid of stop words
        tokens = [theStemmer.stem(word) for word in tokens] #stem words uing porter stemming algorithm
        self.tokens = " ".join(tokens) #need to pass string seperated by spaces       
    
        return self.tokens
    
    def predictClass(self,classes,testDF,vectorizerList,pcaList,model):      
        testDFDescList = testDF['description'].tolist()
        testDFTweetList = testDF['tweet_text'].tolist()
        testDFStatusList = testDF['status_text'].tolist()
        testDFFollowList = testDF['following_descriptions'].tolist()
        
        testDFDescTrans = vectorizerList[0].transform(testDFDescList)
        testDFDescTrans_new = pd.DataFrame(pcaList[0].transform(testDFDescTrans.toarray()))
        
        testDFTweetTrans = vectorizerList[1].transform(testDFTweetList)
        testDFTweetTrans_new = pd.DataFrame(pcaList[1].transform(testDFTweetTrans.toarray()))
        
        testDFStatusTrans = vectorizerList[2].transform(testDFStatusList)
        testDFStatusTrans_new = pd.DataFrame(pcaList[2].transform(testDFStatusTrans.toarray()))
        
        testDFFollowTrans = vectorizerList[3].transform(testDFFollowList)
        testDFFollowTrans_new = pd.DataFrame(pcaList[3].transform(testDFFollowTrans.toarray()))
        
        testDF = testDF.drop(['description','following_descriptions','tweet_text','status_text'], axis=1)
        normalized_testDF = pd.DataFrame(preprocessing.normalize(testDF))
        
        testDFList = [normalized_testDF,testDFDescTrans_new,testDFTweetTrans_new,testDFStatusTrans_new,testDFFollowTrans_new]
        finalTestDF = pd.DataFrame(index=normalized_testDF.index)
        
        for DF in testDFList:
            finalTestDF = pd.concat([finalTestDF,DF], ignore_index=True, axis=1)
        
        x = model.predict(finalTestDF)
        xProba = pd.DataFrame(model.predict_proba(finalTestDF))
        xProba = xProba.round(4) 
        xProba.columns=classes
        xProbaDict = xProba.to_dict('index')
        
        keyPreds={}
        for key,value in xProbaDict.iteritems():
            valMax = max(value.values())
            for cat in value.keys():
                if value[cat]==valMax:
                    keyPreds[key]=cat
        
        predAgeCol = keyPreds.values()
        testDFwithRes = pd.DataFrame({'predictedAges': predAgeCol})
        testDFwithRes.index = testDF.index
        
        return testDFwithRes