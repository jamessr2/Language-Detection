__author__ = 'Lithium'

import urllib2

csvFilename = 'dataSourceWebService.csv'
userAgentString = 'User-agent', 'Mozilla/5.0'
wikiPediaRandomPages = [['ENGLISH','http://en.wikipedia.org/wiki/Special:Random'],['SPANISH','http://es.wikipedia.org/wiki/Especial:Aleatoria']]
numPagesToLoad = 2


def get_random_page(file, wiki, language):
    try:
        # get page and stuff
        opener = urllib2.build_opener()
        opener.addheaders = [(userAgentString)]
        infile = opener.open(wiki)
        url = infile.geturl()[7:]
        file.write('TRUE,' + url + ',' + language + '\n')
    except Exception:
        print('Error page: ' + wiki + ' lang: ' + language) # Page Failed to open

fh = open(csvFilename, 'a')
for item in wikiPediaRandomPages:
    lang = item[0]
    page = item[1]
    for x in range(0,numPagesToLoad):
        get_random_page(fh,page,lang)