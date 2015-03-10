__author__ = 'Lithium'
import urllib.request
import codecs
import re

fname = 'dataSourceWebService.csv'

with open(fname) as f:
    content = [line.rstrip('\n') for line in f]

fileExtension = '.txt'
outputPath = 'data/plaintext/'
webService = 'http://ec2-54-172-230-29.compute-1.amazonaws.com/?url='

#Each line are in the format "[0,1],[url],[language],[outputFileName]"
for line in content:
    splitLine = line.split(',')
    update = splitLine[0]
    url = webService + splitLine[1]
    lang = splitLine[2].upper()
    outputFile = outputPath + lang + '-' + splitLine[3] + fileExtension
    if update.lower() == 'true':
        response = urllib.request.urlopen(url)
        data = response.read()      # a `bytes` object
        text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
        with codecs.open(outputFile,'w', encoding="utf-8") as file:
            file.write("%s\n" % lang)
            file.write(text)
