__author__ = 'Lithium'
import urllib2
import codecs
import time

fname = 'dataSourceWebService.csv'
sleepTime = 1 #In Seconds

with codecs.open(fname, "r", "utf-8") as f:
    content = [line.rstrip('\n') for line in f]

fileExtension = '.txt'
outputPath = 'data/plaintext/'
webService = 'http://ec2-54-172-230-29.compute-1.amazonaws.com/?url='

#Each line are in the format "[0,1],[url],[language]"
for line in content:
    line = line.rstrip('\r') #Remove carriage returns from manual edits
    splitLine = line.split(',')
    update = splitLine[0]
    url = webService + splitLine[1]
    lang = splitLine[2].upper() #remove return character
    outputFile = outputPath + lang + '-' + url.split('/')[-1] + fileExtension
    if update.lower() == 'true':
        time.sleep(sleepTime)
        response = urllib2.urlopen(url)
        data = response.read()      # a `bytes` object
        text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
        with codecs.open(outputFile,'w', encoding="utf-8") as file:
            file.write("%s\n" % lang)
            file.write(text)
