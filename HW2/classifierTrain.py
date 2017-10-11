from classifier import *

#Input directory path to training data
thePath = os.path.abspath("classify")
thePath+="/"
#Path to 'classifierLUT.csv'
thePathLut = os.path.dirname(os.path.abspath(__file__))
thePathLut+="/"

theCols = os.walk(thePath).next()[1]  
theLabels = theCols 

finalWords = list()
theDocs = list()
    
classifyObj = theClassifier()

for word in theCols:
    cnt = 0
    for file in os.listdir(thePath+word):
        if file.endswith('.txt'):
            try:
                f = open(thePath + word + "/" + file, "r")
                lines = f.readlines()
                lines = [text.strip() for text in lines]
                lines = " ".join(lines)
                finalWords.append(classifyObj.genCorpus(lines))
                theDocs.append(classifyObj.textToNum(theLabels,word) +"_" + str(cnt))
                cnt = cnt +  1
            except:
                pass

tdm = classifyObj.vec(finalWords,1000,1,1,theDocs)

reducedTDM = classifyObj.pca(tdm,0.95,theDocs)

fullIndex = reducedTDM.index.values
fullIndex = [int(word.split("_")[0]) for word in fullIndex]

#Training a RF model and outputing to a file for future use in predicting classes
classifyObj.modelTrain(['RF'],reducedTDM,fullIndex,10,thePathLut)