#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 06:37:16 2017

@author: harsheelsoin
"""

import os
os.chdir('/Users/harsheelsoin/Downloads/Projects in Data Science/HomeWork5')

from getDataClass import *
from transformTestData import *
from classifierNew import *
from predictorNew import *

#declaring a training data fetch object
getDataObj = getData()
path = os.getcwd()
path+='/HW5/'
userTrainMetaDict2 = getDataObj.getMeta(path,'user_age_profiles.json','user_age_tweets.json','friend_profiles.json','user_ages_train.csv','friends.csv')
userTrainDF2 = getDataObj.getDF(userTrainMetaDict2)

#declaring a classifier object
classifyObj = theClassifier()

finalTrainDF,classes,vecList,pcaList,fullIndex = classifyObj.prepDataForClass(userTrainDF2)

current_directory = os.getcwd()
mainPath = current_directory+'/'

#training a RF model
model = classifyObj.modelTrain(['RF'],finalTrainDF,fullIndex,5,mainPath)

#declaring a testing data fetch object
getTestDataObj=getTestData()
testDataMeta = getTestDataObj.getTestMeta(path,'user_age_profiles.json','user_age_tweets.json','friend_profiles.json','user_ages_test.csv','friends.csv')
testDF = getTestDataObj.getTestDF(testDataMeta)

#declaring a predictor object
predictObj = thePredictor()

#obtaining predictions for test data and storing in CSV
testDataPredictions = predictObj.predictClass(classes,testDF,vecList,pcaList,model)
testDataPredictions.to_csv('testDataPredictions.csv', sep=',')