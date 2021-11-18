from bs4 import BeautifulSoup
import requests
from Common import DatabaseConnection as dbc

baseUrl = 'https://taz.de'
articleUrl = []

'''
Get a soup contruct for a ressort
IN: ressort = URL of one ressort for example sports
OUT: soup = readable html
'''
def getSoupConstruction(ressort):
    try:
        ressort = requests.get(ressort)
        soup = BeautifulSoup(ressort.content, 'html.parser')
        return soup
    except:
        print("incorrect url")

'''
Crawling all article for a ressort
IN: soup = readable html
OUT: articleUrl = list of all arcticle for a ressort
'''
def crawlingArticlesUrl(soup):
    for a in soup.find_all('a', href=True, role='link'):
        if 'blogs' not in a['href'] and 'campaign' not in a['href'] and 'e-kiosk' not in a['href']: #delete abos, blogs and advertisment
            articleUrl.append(baseUrl + a['href'])
    return articleUrl

'''
Get article number of an article
IN: articleUrl = URL of an specific article
OUT: articleNumber = number of an specific article
'''
def getArticleNumber(articleUrl):
    length = len(articleUrl)
    articleNumber = articleUrl[length - 8:length - 1]
    return articleNumber

'''
Stores raw htmls of all article 
IN: allRessortsUrls = URLs of all ressorts
'''
def storeRawHtml(allRessortsUrls):
    for i in range(0, len(allRessortsUrls)):
        soupArticle = getSoupConstruction(allRessortsUrls[i][0])
        articleUrls = crawlingArticlesUrl(soupArticle)
    for j in range(0, len(articleUrls)):
        #articleNumber = getArticleNumber(articleUrls[j])
        if articleUrls[j]:
            soupArticle = getSoupConstruction(articleUrls[j])

            soupArticleAsString = str(soupArticle)

            key = {"_id": articleUrls[j]}
            data = {"_id": articleUrls[j], "rawhtml": soupArticleAsString}
            dbc.collectionTazData.replace_one(key, data, upsert=True)

'''
Scrape raw html 
IN: allRessortsUrls = URLs of all ressorts
'''
def scrapeRawHtml(allRessortsUrls):
    storeRawHtml(allRessortsUrls)


