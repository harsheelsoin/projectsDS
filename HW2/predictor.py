# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.externals import joblib
import sys
import nltk
from nltk.corpus import stopwords
import re
import os
import operator

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
    
    def predictClass(self,path,theCols,testText):
        vectorizer = joblib.load(path + 'vectorizer.pk') 
        pca = joblib.load(path + 'pca.pk') 
        for file in os.listdir(path):
            if file.endswith(".pkl"):
                theFile = file
        model = joblib.load(path + theFile) #manual for now      
        test = vectorizer.transform(testText)
        X2_new = pca.transform(test.toarray())
        x = model.predict(X2_new)
        xProba = pd.DataFrame(model.predict_proba(X2_new))
        xProba = xProba.round(4) 
        xProba.columns=theCols
        xProbaDict = xProba.to_dict()
        predClass = max(xProbaDict.iteritems(), key=operator.itemgetter(1))[0]
        return predClass
