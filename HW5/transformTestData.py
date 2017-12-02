#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 04:19:25 2017

@author: harsheelsoin
"""

import os
import numpy as np
from numpy import nan
import pandas as pd
import json
import unicodedata
import re
import string

class getTestData():
    
    def textProcess(self,sample):
        sample = sample.strip()
        sample = sample.lower()
        sample = re.sub('[^A-Za-z0-9\.\,]+', ' ', sample)
        sample = sample.translate(None, string.punctuation)
        return sample
    
    def getTestMeta(self,path,userProfileJson,userTweetJson,friendProfileJson,userAgeTestCSV,friendsCSV):
        user_ages_test = pd.read_csv(path+userAgeTestCSV)
        user_ages_test_list = user_ages_test['ID'].tolist()
        with open(path+userProfileJson) as data_file:    
            user_profiles = json.load(data_file)
        with open(path+userTweetJson) as data_file_1:    
            user_tweets = json.load(data_file_1)
        with open(path+friendProfileJson) as data_file_2:    
            friend_profiles = json.load(data_file_2)
        
        friend_profiles_dict={}
        for i in range(0,len(friend_profiles)):
            try:
                ID = friend_profiles[i]['id']
                if ID is not None:
                    friend_profiles_dict[ID]=friend_profiles[i]
            except:
                pass
        
        friends_df = pd.read_csv(path+friendsCSV)
        friends_df2 = friends_df.groupby('ID')['FriendID'].apply(list).reset_index(name='friendsFollowing')
        friendsFollowing_dict = friends_df2.set_index('ID').to_dict()
        friendsFollowing_dict=friendsFollowing_dict['friendsFollowing']
        
        allFriendLists={}
        for ID in user_ages_test_list:
            try:
                reqList = friendsFollowing_dict[ID]
                allFriendLists[ID]=reqList
            except:
                pass
        
        userTestData={}
        for ID,value in allFriendLists.iteritems():
            try:
                reqItem = (item for item in user_profiles if item["id"] == ID).next()
                reqItem2 = (item for item in user_tweets if item["user"]["id"] == ID).next()
                thisDict={}
                valueDict=dict.fromkeys(value)
                if all(v is not None for v in [reqItem,reqItem2]):
                    thisDict['user_profile']=reqItem
                    thisDict['tweet_profile']=reqItem2
                    thisDict['friends_following_profiles']=valueDict
                    userTestData[ID]=thisDict
            except:
                pass
        
        for ID,data in userTestData.iteritems():
            for friendID,value in data['friends_following_profiles'].iteritems():
                try:
                    reqObj = friend_profiles_dict[friendID]
                    userTestData[ID]['friends_following_profiles'][friendID] = reqObj
                except:
                    pass
        
        for ID,data in userTestData.iteritems():
            for friendID in data['friends_following_profiles'].keys():
                if data['friends_following_profiles'][friendID] is None:
                    del data['friends_following_profiles'][friendID]
        
        return userTestData
    
    def getTestDF(self,userTestData):

        userProfileFeatures = ['created_at','favourites_count','followers_count','friends_count','description','listed_count','location','name','profile_use_background_image','protected','profile_background_tile','profile_background_color','screen_name','statuses_count','status']
        
        selUserTestData={}
        for ID,data in userTestData.iteritems():
            thisDict={}
            for key,value in data['user_profile'].iteritems():
                if key in userProfileFeatures:
                    if key=='status':
                        thisDict['status_text']=value['text']
                    else:
                        thisDict[key]=value
            for key,value in data['tweet_profile'].iteritems():
                if key=='text':
                    thisDict['tweet_text']=value
            allDescriptions=""
            for key,value in data['friends_following_profiles'].iteritems():
                thisDesc = value['description']
                thisDesc+=" "
                allDescriptions+=thisDesc
            thisDict['following_descriptions']=allDescriptions
            selUserTestData[ID]=thisDict
        
        for ID,data in selUserTestData.iteritems():
            for key,value in data.iteritems():
                if isinstance(value, unicode):
                    selUserTestData[ID][key] = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
                if isinstance(value, bool):
                    selUserTestData[ID][key] = int(value)
        
        textProcessKeys = ['description','following_descriptions','tweet_text','name','location','status_text','screen_name']
        for ID,data in selUserTestData.iteritems():
            for key,value in data.iteritems():
                if key=='created_at':
                   selUserTestData[ID][key]=int(value[-4:])
                elif key in textProcessKeys:
                    selUserTestData[ID][key]=self.textProcess(value)
                elif key=='profile_background_color':
                    selUserTestData[ID][key]=int(value, 16)
        
        testDF = pd.DataFrame.from_dict(selUserTestData, orient='index')
        userTestDF = testDF.drop(['name','location','screen_name'], axis=1)
        userTestDF2 = userTestDF
        userTestDF2=userTestDF2.replace(to_replace="", value=np.nan).dropna()
        
        return userTestDF2