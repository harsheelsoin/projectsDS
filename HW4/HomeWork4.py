#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 00:24:11 2017

@author: harsheelsoin
"""

import os
os.chdir('/Users/harsheelsoin/Downloads/Projects in Data Science/HomeWork4')
from predictorNew import *
from classifierNew import *
import pandas as pd
import numpy as np
import string
#import imp

#foo = imp.load_source('classifier', '/Users/harsheelsoin/Downloads/Projects in Data Science/HomeWork4')

fields = ['Company','Industry']
df = pd.read_csv('private us companies.csv', skipinitialspace=True, usecols=fields)
df2 = df.groupby('Industry')['Company'].apply(list).reset_index(name='companyList')

testDict = df2.to_dict('index')
#testDict2 = df4.to_dict('split')
#testDict3 = df4.to_dict('records')

industrySamples={}
for i in range(0,len(testDict)):
    data = testDict[i]['companyList']
    if len(data)<100:
        sample = np.random.choice(data, size=100, replace=True)
    else:
        sample = np.random.choice(data, size=100, replace=False)
    sample=list(sample)
    industrySamples[testDict[i]['Industry']] = sample

classes = []
for key, value in industrySamples.iteritems():
    classes.append(key)

theLabels = classes
finalWords = list()
theDocs = list()

classifyObj = theClassifier()

for word in classes:
    cnt=0
    for sample in industrySamples[word]:
        sample = sample.strip()
        sample = sample.lower()
        sample = sample.decode('unicode_escape').encode('ascii','ignore')
        sample = sample.translate(None, string.punctuation)
        finalWords.append(sample)
        theDocs.append(classifyObj.textToNum(theLabels,word) +"_" + str(cnt))
        cnt+=1

tdm, vectorizer = classifyObj.vec(finalWords,1000,1,1,theDocs)
reducedTDM, PCA = classifyObj.pca(tdm,0.95,theDocs)
fullIndex = reducedTDM.index.values
fullIndex = [int(word.split("_")[0]) for word in fullIndex]

current_directory = os.getcwd()
mainPath = current_directory+'/'
model = classifyObj.modelTrain(['RF'],reducedTDM,fullIndex,10,mainPath)

predictObj = thePredictor()

while(True):
    x = raw_input("Enter company name (input nothing to break loop):")
    if x == "":
        print "You didn't give any input, breaking loop"
        break
    else:
        print "Your input is: %s" %x
        tempText = x.strip()
        tempText = tempText.lower()
        tempText = tempText.decode('unicode_escape').encode('ascii','ignore')
        tempText = tempText.translate(None, string.punctuation)
        tempText = tempText.split(" ")
        thePredictedClass = predictObj.predictClass(mainPath,classes,tempText,vectorizer,PCA,model)
        print "The predicted class is: %s" %thePredictedClass