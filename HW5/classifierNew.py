import sklearn
import numpy as np
import nltk
import os
import re
import pickle
import time
import pandas as pd
from sklearn import decomposition
from sklearn.model_selection import cross_val_score
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,BaggingClassifier,GradientBoostingClassifier
from sklearn.manifold import Isomap
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import RidgeClassifier,Lasso,SGDClassifier,LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords,wordnet
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

class theClassifier(object):
    
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
    
    def textToNum(self,theLabels,thePredLabel):
        theOutLabel = dict()
        cnt = 0
        for word in theLabels:
            theOutLabel[word] = cnt
            cnt = cnt + 1
        return str(theOutLabel[thePredLabel])    
    
    def algoArray(self,theAlgo,thePathLut):
        self.theLUT = pd.read_csv(thePathLut + 'classifierLUT.csv',index_col=0) #ALGO LUT
        theAlgoOut = self.theLUT.loc[theAlgo,'functionCall']
        return theAlgoOut

    def vec(self,varData,maxF,nGramMin,nGramMax,theDocs):
        vectorizer = TfidfVectorizer(max_features=maxF,ngram_range=(nGramMin,nGramMax))
        tdm = pd.DataFrame(vectorizer.fit_transform(varData).toarray())
        tdm.columns=vectorizer.get_feature_names()
        tdm.index=theDocs
        return tdm, vectorizer

    def pca(self,varData,varExp,theDocs):
        pca = decomposition.PCA(n_components=varExp)
        pca.fit(varData)
        reducedTDM = pd.DataFrame(pca.transform(varData)) #reduced tdm distance matrix
        reducedTDM.index=theDocs
        return reducedTDM, pca

    def optFunc(self,theAlgo,theParams):
        theModel = self.theLUT.loc[theAlgo,'optimizedCall']
        tempParam = list()
        for key, value in theParams.iteritems():
            tempParam.append(str(key) + "=" + str(value)) 
        theParams = ",".join(tempParam)
        theModel = theModel + theParams + ")"
        return theModel 

    def prepDataForClass(self,userTrainDF2):
        descsDF = userTrainDF2.groupby('age')['description'].apply(list).reset_index(name='descriptionList')
        descsDict = descsDF.to_dict('index')
        
        tweetsDF = userTrainDF2.groupby('age')['tweet_text'].apply(list).reset_index(name='tweetTextList')
        tweetsDict = tweetsDF.to_dict('index')
        
        statusDF = userTrainDF2.groupby('age')['status_text'].apply(list).reset_index(name='statusTextList')
        statusDict = statusDF.to_dict('index')
        
        followingDF = userTrainDF2.groupby('age')['following_descriptions'].apply(list).reset_index(name='followingDescList')
        followingDict = followingDF.to_dict('index')
        
        classes = descsDF['age'].tolist()
        
        finalWordsDesc = list()
        finalWordsTweets = list()
        finalWordsStatus = list()
        finalWordsFollowing = list()
        theDocs = list()
        
        for i in range(0,len(descsDict)):
            dataListDesc = descsDict[i]['descriptionList']
            dataListTweets = tweetsDict[i]['tweetTextList']
            dataListStatus = statusDict[i]['statusTextList']
            dataListFollowing = followingDict[i]['followingDescList']
            for j in range(0,len(dataListDesc)):
                finalWordsDesc.append(dataListDesc[j])
                finalWordsTweets.append(dataListTweets[j])
                finalWordsStatus.append(dataListStatus[j])
                finalWordsFollowing.append(dataListFollowing[j])
                theDoc = str(i)+'_'+str(j)
                theDocs.append(theDoc)
        
        tdmDesc,vecDesc = self.vec(finalWordsDesc,1000,1,1,theDocs)
        reducedTDMDesc, PCADesc = self.pca(tdmDesc,0.95,theDocs)
        
        tdmTweets,vecTweets = self.vec(finalWordsTweets,1000,1,1,theDocs)
        reducedTDMTweets, PCATweets = self.pca(tdmTweets,0.95,theDocs)
        
        tdmStatus,vecStatus = self.vec(finalWordsStatus,1000,1,1,theDocs)
        reducedTDMStatus, PCAStatus = self.pca(tdmStatus,0.95,theDocs)
        
        tdmFollow,vecFollow = self.vec(finalWordsFollowing,1000,1,1,theDocs)
        reducedTDMFollow, PCAFollow = self.pca(tdmFollow,0.95,theDocs)
        
        vecList = [vecDesc,vecTweets,vecStatus,vecFollow]
        pcaList = [PCADesc,PCATweets,PCAStatus,PCAFollow]
        
        fullIndex = reducedTDMDesc.index.values
        fullIndex = [int(word.split("_")[0]) for word in fullIndex]
        
        userTrainDF2 = userTrainDF2.drop(['description','following_descriptions','tweet_text','status_text'], axis=1)
        numFeaturesDFs = userTrainDF2.groupby('age')
        
        newDF = pd.DataFrame(columns=['profile_background_tile','statuses_count','friends_count','profile_use_background_image','age','listed_count','followers_count','protected','profile_background_color','favourites_count','created_at'])
        
        for DF in numFeaturesDFs:
            theDF = DF[1]
            newDF = pd.concat([newDF,theDF])
            
        newDF = newDF.drop(['age'], axis=1)
        normalized_newDF = pd.DataFrame(preprocessing.normalize(newDF))
        normalized_newDF.index=theDocs
        
        DFList = [normalized_newDF,reducedTDMDesc,reducedTDMTweets,reducedTDMStatus,reducedTDMFollow]
        
        finalTrainDF = pd.DataFrame(index=normalized_newDF.index)
        
        for DF in DFList:
            finalTrainDF = pd.concat([finalTrainDF, DF], ignore_index=True, axis=1)
        
        return finalTrainDF,classes,vecList,pcaList,fullIndex
    
    def modelTrain(self,modAr,redTdm,fullInd,fld,thePathLut):
        self.fullInd = fullInd
        theModels = modAr #these MUST match up with names from LUT
        theResults = pd.DataFrame(0,index=theModels,columns=['accuracy','confidence','runtime'])
        for theModel in theModels:
            startTime = time.time()
            model = eval(self.algoArray(theModel,thePathLut))
            print(theModel)
        
            #cross validation    
            cvPerf = cross_val_score(model,redTdm,self.fullInd,cv=fld)
            theResults.ix[theModel,'accuracy'] = round(cvPerf.mean(),2)
            theResults.ix[theModel,'confidence'] = round(cvPerf.std() * 2,2)
            endTime = time.time()
            theResults.ix[theModel,'runtime'] = round(endTime - startTime,0)
            
        print(theResults)
        
        #Run with best performing model, fine tune algorithm grid search
        bestPerfStats = theResults.loc[theResults['accuracy'].idxmax()]
        modelChoice = theResults['accuracy'].idxmax()
                      
        startTime = time.time()
        model = eval(self.algoArray(modelChoice,thePathLut))
        grid = GridSearchCV(estimator=model, param_grid={"n_estimators": [10,30,50,100]})#eval(gridSearch(modelChoice))
        grid.fit(redTdm,self.fullInd)
        bestScore = round(grid.best_score_,4)
        parameters = grid.best_params_
        endTime = time.time()
        print("Best Score: " + str(bestScore) + " and Grid Search Time: " + str(round(endTime - startTime,0)))
        
        #Train best model on data set and save for future use
        startTime = time.time()
        model = eval(self.optFunc(modelChoice,parameters)) #train fully validated and optimized model
        model.fit(redTdm,self.fullInd)
        endTime = time.time()
        print("Model Save Time: " + str(round(endTime - startTime,0)))
        
        return model