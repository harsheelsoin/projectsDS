import numpy as np 
import os
import re
import nltk
import collections
from nltk.corpus import stopwords
from collections import Counter
import csv

cnt=0
cnt2=0

#Input directory path to original files
inputPath = os.path.abspath("classify")

#Output directory path to concatenated category-wise pre-processed files
outputPath = os.path.abspath("classify_out")

theFolders = os.walk(inputPath).next()[1]

def preProcess(theLines):
	#set dictionaries
	stopWords = set(stopwords.words('english'))
	#pre-processing of text
	theLines = theLines.split()
	tokens = [token.lower() for token in theLines] #ensures everything is in lower case
	tokens = [re.sub(r'[^a-zA-Z0-9]+', ' ',token) for token in tokens] #removes special characters leaving word as it is
	tokens = [token for token in tokens if token.lower().isalpha()] #ensures everything is a letter
	tokens = [word for word in tokens if word not in stopWords] #rid of stop words
	tokens = " ".join(tokens) #need to pass string seperated by spaces
	return tokens

for folder in theFolders:
	out = open(outputPath+'/'+folder+'.txt','w')
	for file in os.listdir(inputPath+'/'+folder):
		if file.endswith('.txt'):
			cnt +=1
			inp =open(inputPath+'/'+folder+'/'+file,'r')
			lines = inp.readlines()
			lines = [text.strip() for text in lines]
			lines = " ".join(lines)
			lines = preProcess(lines)

			for line in lines:
				out.write(line)

#Print count to ensure all files have been covered
print cnt

for folder in theFolders:
	with open(outputPath+'/'+folder+'.txt','r') as infile:
		cnt2 +=1
		wordcount = Counter(infile.read().split())
		with open(outputPath+'/'+folder+'.csv','w') as csv_file:
			writer=csv.writer(csv_file)
			for key, value in wordcount.items():
				writer.writerow([key, value])

print cnt2