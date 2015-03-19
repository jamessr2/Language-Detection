from __future__ import print_function
__author__ = 'Lithium'
import urllib2
import codecs
import time

fname = 'dataSourceWebService.csv'
tempFileName = 'dataSourceWebServiceTemp.csv'
sleepTime = 1 #In Seconds

with codecs.open(fname, "r", "utf-8") as f:
    content = [line.rstrip('\n') for line in f]

fileExtension = '.txt'
outputPath = 'data/plaintext/'
webService = 'http://ec2-54-172-230-29.compute-1.amazonaws.com/?url='

numOfPagesInCSV = len(content)
curPageNum = 1
tempFile = codecs.open(tempFileName, "w", "utf-8")
#If the webservice has failed yet
webServiceFailed = False

#Each line are in the format "[0,1],[url],[language]"
for line in content:
    print('Page %d of %d: '% (curPageNum,numOfPagesInCSV), end='')
    curPageNum += 1
    line = line.rstrip('\r') #Remove carriage returns from manual edits
    splitLine = line.split(',')
    update = splitLine[0]
    queryUrl = splitLine[1]
    #If the leading character is / remove it.
    if(queryUrl[0] == '/'):
        queryUrl = queryUrl[1:]

    url = webService + queryUrl
    lang = splitLine[2].upper() #remove return character
    outputFile = outputPath + lang + '-' + url.split('/')[-1]
    #Truncate filename if greater than 170 characters
    if len(outputFile) > 170:
        outputFile = outputFile[:170]
    outputFile += fileExtension
    #Download plaintext if the file indicates it should be updated or the webservice was rejected by wikipedia
    if update.lower() == 'true' and not webServiceFailed:
        print('Downloading and Parsing %s in %s'% (queryUrl,lang))
        time.sleep(sleepTime)
        try:
            response = urllib2.urlopen(url)
            data = response.read()      # a `bytes` object
            text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
            with codecs.open(outputFile,'w', encoding="utf-8") as file:
                file.write("%s\n" % lang)
                file.write(text)
            #Plaintext loaded successfully don't download again
            tempFile.write('FALSE' + ',' + queryUrl + ',' + lang + '\n')
        except urllib2.HTTPError, e:
            #Webservice was denied output error
            webServiceFailed = True
            print('===============Download denied by Wikipedia terminating future downloads=========')
            tempFile.write(update + ',' + queryUrl + ',' + lang + ',' + 'FAILED HERE' + '\n')
    else:
        print('Page %s skipped' % (queryUrl))
        tempFile.write(update + ',' + queryUrl + ',' + lang + '\n')
tempFile.close()

#Copy temp file to csv file
with codecs.open(tempFileName, "r", "utf-8") as tempCSV:
    with codecs.open(fname, "w", "utf-8") as sourceCSV:
        for line in tempCSV:
            sourceCSV.write(line)