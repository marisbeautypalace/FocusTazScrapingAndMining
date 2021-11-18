from textblob_de import TextBlobDE as TextBlob
import pandas as pd
from Common import DatabaseConnection as dbc
from Common import DataOperations as do

bodysFocus = do.getBodys(dbc.collectionFocusData)
bodysTaz = do.getBodys(dbc.collectionTazData)
bodysAll = bodysFocus + bodysTaz

print(bodysTaz)

allTextsFocus = ""
for text in bodysFocus:
     allTextsFocus = allTextsFocus + text

print(TextBlob(allTextsFocus).sentiment)

allTextsTaz = ""
for text in bodysTaz:
    allTextsTaz = allTextsTaz + text

print(TextBlob(allTextsTaz).sentiment)


MostSimilarWordsSustainabilityGermanModel = ['nachhaltiges Wirtschaften',
                                             'oekologische Nachhaltigkeit',
                                             'ökologische Nachhaltigkeit',
                                             'Regionalitaet',
                                             'Regionalität',
                                             'Umweltschutz',
                                             'Energieeffizienz',
                                             'regionale Wertschoepfung',
                                             'regionale Wertschöpfung',
                                             'Ressourcenschonung',
                                             'fairer Handel',
                                             'Ressourceneffizienz',
                                             'nachhaltiges Handeln',
                                             'Nachhaltigkeit'
                                             ]
'''
Get list with bodys which contains a hitword
IN: df = dataframe of a collection (json files from mongodb)
list = list with hitwords
OUT: articlesMatchedHitwords = list of bodys which contains a hitword
'''
def getListForBodysForWordsInList(df, list):
    dfBody = df.body
    articlesMatchedHitwords = []
    contains = False
    for i in range(0, dfBody.size):
        bodyToInvestigate = dfBody[i]
        for j in range(0, len(list)):
            if list[j] in bodyToInvestigate:
                contains = True
        if contains:
            articlesMatchedHitwords.append(bodyToInvestigate)
            contains = False
    return articlesMatchedHitwords

'''
Get list with bodys which not contains a hitword
IN: df = dataframe of a collection (json files from mongodb)
list = list with hitwords
OUT: articlesNotMatchedHitwords = list of bodys which not contains a hitword
'''
def getListForBodysForWordsNotInList(df, list):
    dfBody = df.body
    articlesNotMatchedHitwords = []
    contains = False
    for i in range(0, dfBody.size):
        bodyToInvestigate = dfBody[i]
        for j in range(0, len(list)):
            if list[j] in bodyToInvestigate:
                contains = True
        if not contains:
            articlesNotMatchedHitwords.append(bodyToInvestigate)
        contains = False
    return articlesNotMatchedHitwords

dfTaz = do.transformDataToDf(dbc.collectionTazData)

tazWithSustainibility = getListForBodysForWordsInList(dfTaz, MostSimilarWordsSustainabilityGermanModel)
tazWithoutSustainibility = getListForBodysForWordsNotInList(dfTaz, MostSimilarWordsSustainabilityGermanModel)

dfFocus = do.transformDataToDf(dbc.collectionFocusData)

focusWithSustainibility = getListForBodysForWordsInList(dfFocus, MostSimilarWordsSustainabilityGermanModel)
focusWithoutSustainibility = getListForBodysForWordsNotInList(dfFocus, MostSimilarWordsSustainabilityGermanModel)

def sentimentalanalysesToCsv(polarity, subjectivity, name):
    sentimental = []
    sentimental.append(polarity)
    sentimental.append(subjectivity)
    df = pd.DataFrame(sentimental).transpose()
    df.to_csv(f'Common/data/{name}.csv')

polarity = []
subjectivity = []
nameCSV = ['TazSustainibility', 'TazNotSustainibility', 'FocusSustainibility', 'FocusNotSustainibility']
listSentimentalAnalysis = [tazWithSustainibility, tazWithoutSustainibility, focusWithSustainibility, focusWithoutSustainibility]

for i in range(0, len(listSentimentalAnalysis)):
    for text in listSentimentalAnalysis[i]:
        polarity.append(TextBlob(text).sentiment[0])
        subjectivity.append(TextBlob(text).sentiment[1])

    sentimentalanalysesToCsv(polarity, subjectivity, nameCSV[i])
    polarity.clear()
    subjectivity.clear()
