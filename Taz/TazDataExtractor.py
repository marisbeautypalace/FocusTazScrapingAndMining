from bs4 import BeautifulSoup
import requests
from Common import DatabaseConnection as dbc

'''
Get a soup contruct for a resort
IN: resort = URL of one resort for example sports
OUT: soup = readable html
'''
def getSoupConstruction(resort):
    try:
        resort = requests.get(resort)
        soup = BeautifulSoup(resort.content, 'html.parser')
        return soup
    except:
        print("incorrect url")

'''
Get titel and subtitle of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: headline = title and subtitle of the article
'''
def getTitleAndSubtitle(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        headline = (soup.find('h1').get_text())
        return headline
    except:
        print("no title extractable")

'''
Get intro of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: intro = summary of an article
'''
def getIntro(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        intro = (soup.find("p", class_="intro").get_text())
        return intro
    except:
        print("no intro extractable")

'''
Get author of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: author = creator of an article
'''
def getAuthor(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        author = (soup.find('h4').get_text())
        return author
    except:
        print("no author extractable")

'''
Get publish date of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: date = date when the article was published
'''
def getDate(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        date = (soup.find("li", class_="date").get_text())
        return date
    except:
        print("no date extractable")

'''
Get ressort of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: ressort = ressort in where the article was published
'''
def getRessort(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        ressort = (soup.find('li', class_='last even trodd selected').get_text())
        return ressort
    except:
        print("no ressort extractable")

'''
Get text of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: body = text of the article
'''
def getBody(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        resort = (soup.find("article", class_="sectbody").get_text())
        return resort
    except:
        print("no body extractable")

'''
Get keywords  of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: keywords = list of the keywords
'''
def getKeywords(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        frameAllTopics = soup.find_all("a", class_="tag dirlink")
        keywords = []
        for i in frameAllTopics:
            keywords.append(i.get_text())
        return keywords
    except:
        print("no keywords extractable")

'''
Extracs and stores data on the basis of rawhtmls
'''
def extractData():
    rawHtmls = dbc.collectionTazRawHtml.find()
    amountOfData = rawHtmls.count()

    for r in range(0, amountOfData):
        rawHtml = rawHtmls[r]

        id = rawHtml['_id']
        date = getDate(rawHtml['rawhtml'])
        author = getAuthor(rawHtml['rawhtml'])
        title = getTitleAndSubtitle(rawHtml['rawhtml'])
        keywords = getKeywords(rawHtml['rawhtml'])
        intro = getIntro(rawHtml['rawhtml'])
        body = getBody(rawHtml['rawhtml'])
        ressort = getRessort(rawHtml['rawhtml'])

        if id and date and author and title and keywords and intro and body and ressort:
            key = {"_id": id}
            data = {"_id": id, "date": date, "author": author, "title":
                    title, "keywords": keywords, "intro": intro, "body": body, "ressort": ressort}
            dbc.collectionTazData.replace_one(key, data, upsert=True)



