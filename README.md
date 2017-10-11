# projectsDS
Submissions for Projects in Data Science

# Homework 1
The three python files correspond to questions 1, 2 and 3 of the first homework.
Python 2.7.13 has been used.

Please download entire directory 'HW1' to run scripts. The scripts will need all folders in directory to get paths for necessary processing. Paths in scripts will be adjusted automatically based on your system once you download this directory.

If issues are still encoutered with paths, kindly use following (for question3.py):

inputPath = <your_download_directory>/HW1/classify/

outputPath = <your_download_directory>/HW1/classify_out

Outputs of my codes are given in the sub-directory: 'outputsObtained' (for your reference).
Latest versions of the same can also be found in the sub-directory 'classify_out'

# Homework 2
The following is a description of the python scripts submitted:

'classifier.py': defines the class 'theClassifier' for training a model using a particular classification technique

'classifierTrain.py': imports the 'theClassifier' class from 'classifier.py' and trains and stores a Random Forest (RF) classification module in working directory, along with vectorizer and pca pickle files

'predictor.py': defines the class 'thePredictor' for predicting the class of any input text into four categories: 'fishing','hiking','machine learning','mathematics'

'streamTweet.py': imports the 'thePredictor' class from 'predictor.py' and defines a class 'StreamListener' using 'tweepy'. This script continously streams tweets and inserts only 100 tweets into the 'twitterDBs' mongo database as a collection called 'theData'. The tweets are stored in JSON format into the 'theData' collection after being classified in Real Time as one of the four categories: 'fishing','hiking','machine learning','mathematics'

After downloading entire HW2 directory, and while running scripts, path objects such as 'thePath', 'thePathLut' (in 'classifierTrain.py') and 'thePath','directoryPath' (in 'streamTweet.py') will be automatically set. The scripts will need all folders and files in HW2 directory to get paths for necessary processing. 

The collection 'theData' (containing 100 tweets post classification) is then exported into a JSON file called 'sample.json' (in current working directory) using the following command in terminal:

mongoexport -d twitterDBs -c theData -o sample.json

I've provided my 'sample.json' output containing 100 tweets with all necessary fields (along with 'topic' obtained post RT classification)
