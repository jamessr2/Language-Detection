__author__ = 'Lithium'
import urllib.request
import codecs
import re

class WikiParser:
    def parse_raw(self, rawText):
        ret = ''
        # [
        skip1c = 0
        # {
        skip2c = 0

        #remove { [ ] } meta data
        for i in rawText:
            if i == '[':
                skip1c += 1
            elif i == '{':
                skip2c += 1
            elif i == ']' and skip1c > 0:
                skip1c -= 1
            elif i == '}' and skip2c > 0:
                skip2c -= 1
            elif skip1c == 0 and skip2c == 0:
                ret += i
        #Remove left over ()
        cleanr =re.compile(r'\(\)')
        cleantext = re.sub(cleanr,'', ret)

        #Remove <ref> text </ref>
        cleanr =re.compile(r'\<ref>(.*?)\</ref>')
        cleantext = re.sub(cleanr,'', cleantext)

        #Remove <ref extra stuff> text </ref>
        cleanr =re.compile(r'\<ref(.*)>(.*?)\</ref>')
        cleantext = re.sub(cleanr,'', cleantext)

        #Remove <ref />
        cleanr =re.compile(r'\<ref(.*)/>')
        cleantext = re.sub(cleanr,'', cleantext)

        #Remove <gallery> text </gallery>
        cleanr =re.compile(r'\<gallery>(.*?)\</gallery>')
        cleantext = re.sub(cleanr,'', cleantext)

        #Replace '' or ''' with '
        cleanr =re.compile(r'\'\'(\'?)')
        cleantext = re.sub(cleanr,'\'', cleantext)

        #Remove titles
        cleanr =re.compile(r'==(=?)(.*?)(=?)==')
        cleantext = re.sub(cleanr,'', cleantext)

        return cleantext

fname = 'dataSource.csv'

with open(fname) as f:
    content = [line.rstrip('\n') for line in f]

fileExtension = '.txt'
urlRawQuery = '?action=raw'

wikiParser = WikiParser();
#Each line are in the format "[0,1],[url],[language],[outputFileName]"
for line in content:
    splitLine = line.split(',')
    update = splitLine[0]
    url = splitLine[1] + urlRawQuery
    lang = splitLine[2]
    outputFile = 'data/' + splitLine[3] + fileExtension
    if update.lower() == 'true':
        response = urllib.request.urlopen(url)
        data = response.read()      # a `bytes` object
        text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
        parsedText = wikiParser.parse_raw(text)
        with codecs.open(outputFile,'w', encoding="utf-8") as file:
            file.write("%s\n" % lang)
            file.write(parsedText)
