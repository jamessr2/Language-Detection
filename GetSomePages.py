__author__ = 'Lithium'

import urllib2, codecs

csvFilename = 'dataSourceWebService.csv'
userAgentString = 'User-agent', 'Mozilla/5.0'
wikiPediaRandomPages = [#['ENGLISH','http://en.wikipedia.org/wiki/Special:Random'],
                        #['SPANISH','http://es.wikipedia.org/wiki/Especial:Aleatoria'],
                        ['FRENCH','http://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard'],
                        ['GERMAN','http://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite'],
                        ['PORTUGUESE','http://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria'],
                        ['FINNISH','http://fi.wikipedia.org/wiki/Toiminnot:Satunnainen_sivu'],
                        ['NORWEGIAN','http://no.wikipedia.org/wiki/Spesial:Tilfeldig'],
                        ['ITALIAN','http://it.wikipedia.org/wiki/Speciale:PaginaCasuale'],
                        ['DUTCH','http://nl.wikipedia.org/wiki/Speciaal:Willekeurig'],
                        ['DANISH','http://da.wikipedia.org/wiki/Speciel:Tilf%C3%A6ldig_side'],
                        ['SWEDISH','http://sv.wikipedia.org/wiki/Special:Slumpsida'],
                        ['ESPERANTO','http://eo.wikipedia.org/wiki/Speciala%C4%B5o:Hazarda_pa%C4%9Do'],
                        ['RUSSIAN','https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'],
                        ['UKRAINIAN','https://uk.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B5%D1%86%D1%96%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0:%D0%92%D0%B8%D0%BF%D0%B0%D0%B4%D0%BA%D0%BE%D0%B2%D0%B0_%D1%81%D1%82%D0%BE%D1%80%D1%96%D0%BD%D0%BA%D0%B0'],
                        ['AFRIKAANS','http://af.wikipedia.org/wiki/Spesiaal:Lukraak'],
                        ['VIETNAMESE','http://vi.wikipedia.org/wiki/%C4%90%E1%BA%B7c_bi%E1%BB%87t:Ng%E1%BA%ABu_nhi%C3%AAn'],
                        ['BOSNIAN','http://bs.wikipedia.org/wiki/Posebno:Slu%C4%8Dajna_stranica'],
                        ['CZECH','http://cs.wikipedia.org/wiki/Speci%C3%A1ln%C3%AD:N%C3%A1hodn%C3%A1_str%C3%A1nka'],
                        ['GAELIC','http://gl.wikipedia.org/wiki/Especial:Ao_chou'],
                        ['POLISH','http://pl.wikipedia.org/wiki/Specjalna:Losowa_strona'],
                        ['SERBIAN','http://sr.wikipedia.org/wiki/%D0%9F%D0%BE%D1%81%D0%B5%D0%B1%D0%BD%D0%BE:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D1%98%D0%BD%D0%B0%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B0'],
                        ['SWAHILI','http://sw.wikipedia.org/wiki/Maalum:UkurasawaBahati'],
                        ['WELSH','http://cy.wikipedia.org/wiki/Arbennig:Random'],
                        ['TAGALOG','http://tl.wikipedia.org/wiki/Natatangi:Alin_man'],
                        ['GREEK','http://el.wikipedia.org/wiki/%CE%95%CE%B9%CE%B4%CE%B9%CE%BA%CF%8C:%CE%A4%CF%85%CF%87%CE%B1%CE%AF%CE%B1'],
                        ['ARABIC','http://ar.wikipedia.org/wiki/%D8%AE%D8%A7%D8%B5:%D8%B9%D8%B4%D9%88%D8%A7%D8%A6%D9%8A'],
                        ['KURDISH','http://ckb.wikipedia.org/wiki/%D8%AA%D8%A7%DB%8C%D8%A8%DB%95%D8%AA:%DA%BE%DB%95%DA%B5%DA%A9%DB%95%D9%88%D8%AA%D8%8C%D9%BE%DB%95%DA%95%DB%95%DB%8C_%D8%A8%DB%95_%DA%BE%DB%95%D8%B1%D9%85%DB%95%DA%A9%DB%8C']]
numPagesToLoad = 4


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