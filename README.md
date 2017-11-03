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

# Homework 3
The following is a description of the python scripts submitted:

Kindly note that execution of 'streamLined.py' takes around 10 minutes in general, because of the number of steps and web crawling and scraping involved. Also, please note that the entire HW3 directory needs to be downloaded for execution of 'streamLined.py', as it imports modules from other python scripts in the directory, and model parameters from 'classifierLUT.csv'

Sample data (training data and pickle files generated) post test execution of 'streamLined.py' has been provided in the directory 'sampleStreamLineExecutionData' for reference

Also, please note that before executing 'streamLined.py', the path needs to be changed to the path of the downloaded HW3 directory, as per your system. This needs to be set in 'os.chdir(<path_to_HW3>)' (line 11 of 'streamLined.py')
All other directory objects such as 'current_directory', 'mainPath' and 'theDataPath' will be set automatically by the code

'crawler.py': defines the class 'theCrawler' containing two functions 'theIndexer' and 'dataGenerator'. 'theIndexer' retrieves the required number of URLs through the Google search python module for each of the five topics and returns a list of those URLs. 'dataGenerator' takes the URLs returned by 'theIndexer', scrapes the HTML of those URLs for text, creates a main folder for the training data and subdirectories named according to class category, and dumps the scraped text into text files corresponding to respective class sub-directories. Around 50-60 text files (containing atleast 50 words each) for each classification category will be generated. 'dataGenerator' also returns a list of document word counts for all of the text files generated, for verification of word count criterion.

'classifier.py': defines the class 'theClassifier' for training a model using a particular classification technique

'predictor.py': defines the class 'thePredictor' for predicting the class of any input text into five categories: 'politics','astronomy','medical','music' and 'sports'

'streamLined.py': This script executes the entire system from crawling and data generation to tweet classification. This script imports 'theCrawler' class from 'crawler.py', 'theClassifier' class from 'classifier.py' and 'thePredictor' class from 'predictor.py'. First, the topics are specified for training data generation. A crawler object then crawls Google for those topics generating a list of URLs (sufficiently large) for each of the topics, and scrapes those URLs to generate the training data directory for the classifier. The crawler object also dumps two pickle files: one containing all URLs crawled ('allFileIndices.pkl') and the other containing all document word counts ('allDocWordCount.pkl'), for future use, so that Google doesn't need to be crawled everytime 'streamLined.py' is run (crawling repeatedly involves certain compications with IP being blocked)

A classifier object then uses that training data, trains and stores a Random Forest (RF) classification module in working directory(.pkl file), along with vectorizer and pca pickle files

A predictor object then uses the 'RF.pkl' file (trained model) to predict any arbitrary text provided by the user. A sample text is provided for test classification. The predicted class for the sample text is stored in the variable 'thePredictedClass'

'streamLined.py' then defines a class 'StreamListener' using 'tweepy' for real-time tweet classification into the five categories. the 'StreamListener' class uses a predictor object to predict each tweet's body and label into one of the give categories. Thereafter, tweet entities such as 'followers', 'screen_name', 'friends_count', 'created_at', 'message_id', 'location', 'body' and 'topic' are stored in a mongo DB called 'twitterDBs' in the collection 'theData', as tweets are streamed continously. Once the required number of tweets have been classified, 'streamLined.py' execution can be stopped.

The collection 'theData' is then exported into a JSON file called 'hw3.json' using the following command in terminal (ensure command is executed in current working directory, ie, 'HW3' directory):

mongoexport -d twitterDBs -c theData -o sample.json

A sample json output has been provided in the 'HW3' directory as required, post execution of 'streamLined.py'
