#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 02:18:13 2017

@author: harsheelsoin
"""
import os
import json
import pandas as pd
import unicodedata
import numpy as np
import string
import re

class getData(object):
     
    def textProcess(self,sample):
        sample = sample.strip()
        sample = sample.lower()
        sample = re.sub('[^A-Za-z0-9\.\,]+', ' ', sample)
        sample = sample.translate(None, string.punctuation)
        return sample
    
    def ageToRange(self,age):
        ageBrackets = {0:"18 to 24",1:"25 to 34",2:"35 to 44",3:"45 to 54",4:"55 to 64",5:"65 and above"}
        if 18<=age<=24:
            age = ageBrackets[0]
        elif 25<=age<=34:
            age = ageBrackets[1]
        elif 35<=age<=44:
            age = ageBrackets[2]
        elif 45<=age<=54:
            age = ageBrackets[3]
        elif 55<=age<=64:
            age = ageBrackets[4]
        else:
            age = ageBrackets[5]
        return age
        
    def getMeta(self,path,userProfileJson,userTweetJson,friendProfileJson,userAgeCSV,friendsCSV):
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
        
        user_ages_train = pd.read_csv(path+userAgeCSV)
        user_ages_train_dict = user_ages_train.set_index('ID').to_dict()
        user_ages_train_dict=user_ages_train_dict['Age']
        
        friends_df = pd.read_csv(path+friendsCSV)
        friends_df2 = friends_df.groupby('ID')['FriendID'].apply(list).reset_index(name='friendsFollowing')
        friendsFollowing_dict = friends_df2.set_index('ID').to_dict()
        friendsFollowing_dict=friendsFollowing_dict['friendsFollowing']
    
        allFriendLists={}
        for ID,age in user_ages_train_dict.iteritems():
            try:
                reqList = friendsFollowing_dict[ID]
                allFriendLists[ID]=reqList
            except:
                pass
        
        userTrainData={}
        for ID,value in allFriendLists.iteritems():
            try:
                reqItem = (item for item in user_profiles if item["id"] == ID).next()
                reqItem2 = (item for item in user_tweets if item["user"]["id"] == ID).next()
                thisDict={}
                valueDict=dict.fromkeys(value)
                if all(v is not None for v in [reqItem,reqItem2]):
                    thisDict['age']=user_ages_train_dict[ID]
                    thisDict['user_profile']=reqItem
                    thisDict['tweet_profile']=reqItem2
                    thisDict['friends_following_profiles']=valueDict
                    userTrainData[ID]=thisDict
            except:
                pass
        
        for ID,data in userTrainData.iteritems():
            for friendID,value in data['friends_following_profiles'].iteritems():
                try:
                    reqObj = friend_profiles_dict[friendID]
                    userTrainData[ID]['friends_following_profiles'][friendID] = reqObj
                except:
                    pass
        
        for ID,data in userTrainData.iteritems():
            for friendID in data['friends_following_profiles'].keys():
                if data['friends_following_profiles'][friendID] is None:
                    del data['friends_following_profiles'][friendID]
        
        return userTrainData
            
    def getDF(self,userTrainData):
    
        allFollowingKeys=[]
        for key,data in userTrainData.iteritems():
            for friendID,value in data['friends_following_profiles'].iteritems():
                if friendID not in allFollowingKeys:
                    allFollowingKeys.append(friendID)
    
        userProfileFeatures = ['created_at','favourites_count','followers_count','friends_count','description','listed_count','location','name','profile_use_background_image','protected','profile_background_tile','profile_background_color','screen_name','statuses_count','status']
        selUserTrainData={}
        for ID,data in userTrainData.iteritems():
            thisDict={}
            thisDict['age']=data['age']
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
            selUserTrainData[ID]=thisDict
        
        for ID,data in selUserTrainData.iteritems():
            for key,value in data.iteritems():
                if isinstance(value, unicode):
                    selUserTrainData[ID][key] = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
                if isinstance(value, bool):
                    selUserTrainData[ID][key] = int(value)
        
        textProcessKeys = ['description','following_descriptions','tweet_text','name','location','status_text','screen_name']
        for ID,data in selUserTrainData.iteritems():
            for key,value in data.iteritems():
                if key=='created_at':
                   selUserTrainData[ID][key]=int(value[-4:])
                elif key in textProcessKeys:
                    selUserTrainData[ID][key]=self.textProcess(value)
                elif key=='profile_background_color':
                    selUserTrainData[ID][key]=int(value, 16)
                elif key=='age':
                    selUserTrainData[ID][key]=self.ageToRange(value)
        
        trainDF = pd.DataFrame.from_dict(selUserTrainData, orient='index')
        userTrainDF2 = trainDF.drop(['name','location','screen_name'], axis=1)
        userTrainDF2Copy = userTrainDF2
        userTrainDF2Copy=userTrainDF2Copy.replace(to_replace="", value=np.nan).dropna()
#        trainDF_new = pd.DataFrame(0, index=trainDF.index, columns=allFollowingKeys)
#        trainDFFinal = pd.concat([trainDF,trainDF_new], axis=1)
        
#        for ID,data in userTrainData.iteritems():
#            for friendID,value in data['friends_following_profiles'].iteritems():
#                trainDFFinal.set_value(ID,friendID,1)
        
        return userTrainDF2Copy