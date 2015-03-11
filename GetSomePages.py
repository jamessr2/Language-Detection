__author__ = 'Lithium'

import urllib2, codecs

csvFilename = 'dataSourceWebService.csv'
userAgentString = 'User-agent', 'Mozilla/5.0'
wikiPediaRandomPages = [#['ENGLISH','http://en.wikipedia.org/wiki/Special:Random'],
                        #['SPANISH','http://es.wikipedia.org/wiki/Especial:Aleatoria'],
                        ['ARABIC','http://ar.wikipedia.org/wiki/%D8%AE%D8%A7%D8%B5:%D8%B9%D8%B4%D9%88%D8%A7%D8%A6%D9%8A']]
numPagesToLoad = 2


def get_random_page(file, wiki, language):
    try:
        # get page and stuff
        opener = urllib2.build_opener()
        opener.addheaders = [(userAgentString)]
        infile = opener.open(wiki)
        url = infile.geturl()[7:]
        #Don't add the url if there is a comma in it, because CSV
        if not ',' in url:
            file.write('TRUE,' + url + ',' + language + '\n')
    except Exception:
        print('Error page: ' + wiki + ' lang: ' + language) # Page Failed to open

with codecs.open(csvFilename, "a", "utf-8") as fh:
    for item in wikiPediaRandomPages:
        lang = item[0]
        page = item[1]
        for x in range(0,numPagesToLoad):
            get_random_page(fh,page,lang)