import pickle
import os
import google
import ssl
import urllib2
from bs4 import BeautifulSoup

class theCrawler(object):

    def theIndexer(self, queries, currentPath):    
        allFileIndices=[]
        for query in queries:
            fileIndex = list()
            for url in google.search(query, num=300, start=0, stop=50, pause=2.0):
                fileIndex.append(url)
            allFileIndices.append(fileIndex)
        
        with open(currentPath + '/' + 'allFileIndices.pkl', 'wb') as f:
            pickle.dump(allFileIndices, f)
        
        return allFileIndices

    def dataGenerator(self, allFileIndices, queries, currentPath):
        final_directory = os.path.join(currentPath, r'theData')
        if not os.path.exists(final_directory):
           os.makedirs(final_directory)
        
        allSubDirectories=[]
        for query in queries:
            subDirectory = os.path.join(final_directory, query)
            if not os.path.exists(subDirectory):
                os.makedirs(subDirectory)
            allSubDirectories.append(subDirectory)

        allDocWordCount=[]
        
        for i in range(0,len(queries)):
            cnt = 0
            docWordCount=[]
            for theUrl in allFileIndices[i]:
                if cnt<60:
                    try:
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
                        opener.addheaders = [('Referer', theUrl)]
                        html = opener.open(theUrl,timeout=10).read()
                        soup = BeautifulSoup(html,"lxml")
                        
                        textTemp = list()
                        try:
                            textTemp.append(soup.find('title').text)
                            textTemp.append('\n')
                            for theText in soup.find_all(['p'],text=True): #,'li']):#,'li']):#,'ul']):#,'span']):#,'li']):
                                textTemp.append(theText.text)
                        except:
                            print theUrl
                            pass    
                    
                        text = " " . join(textTemp)
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = '\n'.join(chunk for chunk in chunks if chunk)
                        text = text.encode('utf8')
                        if len(text.split(' '))>=50:
                            docWordCount.append(len(text.split(' ')))
                            tmpFile = str(cnt) + ".txt"
                            indexFile = open(allSubDirectories[i] + "/" + tmpFile, "w")
                            indexFile.write(text)
                            indexFile.close()
                            cnt = cnt + 1
                    except:
                        pass
            allDocWordCount.append(docWordCount)
        
        with open(currentPath + '/' + 'allDocWordCount.pkl', 'wb') as f2:
            pickle.dump(allDocWordCount, f2)
        return allDocWordCount