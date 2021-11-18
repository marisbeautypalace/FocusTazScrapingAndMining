from bs4 import BeautifulSoup
import requests
from Common import DatabaseConnection as dbc

body = []

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
Get titel of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: headline = title and subtitle of the article
'''
def getTitle(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        headline = (soup.find('div', class_='articleIdentH1').get_text())
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
        intro = (soup.find("div", class_="leadIn").get_text())
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
        author = (soup.find("a", rel="author").get_text())
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
        date = (soup.find("div", class_="displayDate").get_text())
        return date
    except:
        print("no date extractable")

'''
Get text of an article
IN: rawHtml = rawhtml of one specific article from crawler
OUT: body = text of the article
'''
def getBody(rawHtml):
    try:
        soup = BeautifulSoup(rawHtml, 'html.parser')
        for a in soup.find_all("div", class_="textBlock"):
            body.append(a.get_text())
        return body

    except:
        print("no body extractable")


'''
Extracs and stores data on the basis of rawhtmls
'''
def extractData():
    rawHtmls = dbc.collectionFocusRawHtml.find()
    amountOfData = rawHtmls.count()

    for r in range(0, amountOfData):
        try:
            rawHtml = rawHtmls[r]

            id = rawHtml['_id']
            date = getDate(rawHtml['rawhtml'])
            author = getAuthor(rawHtml['rawhtml'])
            title = getTitle(rawHtml['rawhtml'])
            intro = getIntro(rawHtml['rawhtml'])
            body = getBody(rawHtml['rawhtml'])
            bodyAsString = ''.join(body)

            if id and bodyAsString and title:
                key = {"_id": id}
                data = {"_id": id, "date": date, "author": author, "title":
                        title, "intro": intro, "body": bodyAsString}
                dbc.collectionFocusData.replace_one(key, data, upsert=True)
            body.clear()
        except:
            print('cant extract focus data')