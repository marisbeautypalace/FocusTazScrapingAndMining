from pymongo import MongoClient

'''
Connection with MongoDB
'''
client = MongoClient('mongodb://localhost:27017/')
db = client.scraper
collectionTazData = db.tazdata
collectionFocusData = db.focusdata
collectionFocusRawHtml = db.focusrawhtml
collectionTazRawHtml = db.tazrawhtml

#test database
dbTest = client.test
collectionTest = dbTest.testdata