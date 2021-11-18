from bs4 import BeautifulSoup
import requests
from Common import DatabaseConnection as dbc

articleUrl = []

'''
Get a soup construct for a resort
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
Crawling all article for a resort
IN: soup = readable html
OUT: articleUrl = list of all arcticle for a resort
'''
def crawlingArticlesUrl(soup):
    for a in soup.find_all('a', href=True):
        articleUrl.append(a['href'])
    return articleUrl

'''
Get article number of an article
IN: articleUrl = URL of an specific article
OUT: articleNumber = number of an specific article
'''
def getArticleNumber(articleUrl):
    length = len(articleUrl)
    articleNumber = articleUrl[length - 13:length - 5]
    return articleNumber

'''
Stores raw htmls of all article 
IN: allRessortsUrls = URLs of all resorts
'''
def storeRawHtml(allRessortsUrls):
    for i in range(0, len(allRessortsUrls)):
        soupResort = getSoupConstruction(allRessortsUrls[i][0])
        allNews = soupResort.find('div', id='notesList')
        allArticleUrls = (crawlingArticlesUrl(allNews))
    for j in range(0, len(allArticleUrls)):
        #articleNumber = getArticleNumber(allArticleUrls[j])
        soupArticle = getSoupConstruction(allArticleUrls[j])
        soupArticleAsStr = str(soupArticle)

        key = {"_id": allArticleUrls[j]}
        data = {"_id": allArticleUrls[j], "rawhtml": soupArticleAsStr}
        dbc.collectionFocusData.replace_one(key, data, upsert=True)

'''
Scrape raw html 
IN: allRessortsUrls = URLs of all resorts
'''
def scrapeRawHtml(allRessortsUrls):
    storeRawHtml(allRessortsUrls)




