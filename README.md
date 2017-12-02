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

mongoexport -d twitterDBs -c theData -o hw3.json

A sample json output has been provided in the 'HW3' directory as required, post execution of 'streamLined.py'

# Homework 4
The Homework 4 submission consists of three scripts:
Note: Please download entire 'HW4' folder, as all files are required for execution. The user needs to change the directory path at the start of the 'HomeWork4.py' code from '/Users/harsheelsoin/Downloads/Projects in Data Science/HomeWork4' to <locally_downloaded_HW4_directory_path>. Also, the execution of 'HomeWork4.py' takes around 25 min (until the point where user inputs for company names are accepted), because of the scale of the data and the large number of classes
1) 'HomeWork4.py': This script takes in the given database of companies and their industry categories, performs random sampling of size 100 from each industry category (without replacement if population for industry>=100 and with replacement if population for industry<100), trains a Random Forest model on this data, and then accepts user inputs (company names) continuously so as to predict the company industry. The user can break this continous loop by giving an empty input
2) 'classifierNew.py': defines the class 'theClassifier' for training a model using a particular classification technique. The difference here is that no pickle files for the vectorizer, PCA or model are being saved. All these objects are stored in run time during execution of 'HomeWork4.py', and not dumped into pickle filed on the hard disk
3) 'predictorNew.py': defines the class 'thePredictor' for predicting the class of any input text (company name) into one of the 99 industry categories

# Homework 5
The Homework 5 submission consists of five scripts:
Note: Please download entire 'HW5' folder submission, and also kindly ensure that dataset folder called 'HW5' is stored within the HW5 directory containing all 5 scripts. The user needs to change the directory path at the start of the 'predictTwitterAge.py' script from '/Users/harsheelsoin/Downloads/Projects in Data Science/HomeWork5' to <locally_downloaded_HW5_directory_path>. Further, because of the scale of the data and number of of features involved, execution of 'predictTwitterAge.py' will take around 5 min. A CSV file is generated by the code in the code's working directory, which contains the predicted age groups of the user IDs in 'user_ages_test.csv'. Further, please note that only those ID ages were predicted for whom complete information was present in the dataset
1) 'getDataClass.py': Script which automates the process of scanning multiple available datasets for useful features about twitter users and returns a meta dictionary of features corresponding to all user IDs (for whom complete information is available) in 'user_ages_train.csv'. Further it also automates the generation of a dataframe in the required format post necessary pre-processing from the meta dictionary
2) 'transformTestData.py': Script which automates the process of scanning multiple available datasets for features used to train the model, corresponding to the test user IDs in 'user_ages_test.csv'. Returns a meta dictionary for the test users and further a testData dataframe in the required format for prediction
3) 'classifierNew.py': defined the class 'theClassifier' for training a model using a particular classification technique. A new function called 'prepDataForClass' has been introduced to process given training data (in dataframe format) and produce vectorizers, PCA objects, and other attributes required for the prediction stage of the project
4) 'predictorNew.py': defines the class 'thePredictor' for predicting the age of a twitter users based on their profiles, taking in a test dataframe and the model object among many other necessary inputs. The 'predictClass' function has been modified to deal with a dataframe instead of simple text inputs, by employing necessary vectorization and PCA implementation on the test dataframe. This function returns a dataframe containing all test User IDs analyzed and their corresponding predicted age groups (18-24, 25-34, 35-44, 45-54, 55-54, 65+) 
5) 'predictTwitterAge.py': Connects all the scripts together. This script when run uses classes and corresponding functions from all other four scripts and solves the problem of predicting ages of twitter users based on their profiles
