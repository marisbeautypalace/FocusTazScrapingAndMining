import csv
import pandas as pd
from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import f_oneway
from sklearn.linear_model import LinearRegression
from Common import DatabaseConnection as dbc
from Common import DataCleaning as dc

notSustainabilityRessortsTaz = ['Politik', 'Deutschland', 'Europa', 'Amerika', 'Afrika', 'Asien', 'Nahost', 'Netzpolitik', 'Gesellschaft', 'Alltag', 'Debatte', 'Kolumnen', 'Medien', 'Bildung', 'Gesundheit', 'Reise', 'Kultur', 'Musik', 'Film', 'Künste', 'Buch', 'Netzkultur', 'Sport', 'Fußball', 'Kolumnen', 'Berlin', 'Nord', 'Hamburg', 'Bremen', 'Kultur', 'Wahrheit']

sustainabilityRessortsTaz = ['Ökonomie', 'Ökologie', 'Arbeit', 'Konsum', 'Verkehr', 'Wissenschaft', 'Netzökonomie']

mainRessortsWithSubressort = [
    ['Deutschland', 'Politik'],
    ['Europa', 'Politik'],
    ['Amerika', 'Politik'],
    ['Afrika', 'Politik'],
    ['Asien', 'Politik'],
    ['Nahost', 'Politik'],
    ['Netzpolitik', 'Politik'],
    ['Oekonomie', 'Oeko'],
    ['Ökonomie', 'Oeko'],
    ['Oekologie', 'Oeko'],
    ['Ökologie', 'Oeko'],
    ['Arbeit', 'Oeko'],
    ['Konsum', 'Oeko'],
    ['Verkehr', 'Oeko'],
    ['Wissenschaft', 'Oeko'],
    ['Netzoekonomie', 'Oeko'],
    ['Netzökonomie', 'Oeko'],
    ['Alltag', 'Gesellschaft'],
    ['Debatte', 'Gesellschaft'],
    ['Kolumnen', 'Gesellschaft'],
    ['Medien', 'Gesellschaft'],
    ['Bildung', 'Gesellschaft'],
    ['Gesundheit', 'Gesellschaft'],
    ['Reise', 'Gesellschaft'],
    ['Musik', 'Kultur'],
    ['Film', 'Kultur'],
    ['Künste', 'Kultur'],
    ['Buch', 'Kultur'],
    ['Netzkultur', 'Kultur'],
    ['Sport', 'Kultur'],
    ['Fußball', 'Kultur'],
    ['Kolumnen', 'Kultur']
]

secondaryRessortsWithSubressorts = ['Berlin', 'Nord', 'Hamburg', 'Bremen', 'Wahrheit','Tom über die Wahrheit']

contingencyCategories = [
    [1, 400],
    [2, 800],
    [3, 1200],
    [4, '>3']
]

'''
Extracs data for map + reduce script FreqAuthor.py
'''
def createDataForFreqAuthor():
    data = dbc.collectionTazData.find()
    amountOfData = data.count()
    with open('data/freqAuthors.data', mode='w', encoding='utf-8') as employee_file:
        for i in range(0, amountOfData):
            writer = csv.writer(employee_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([data[i]['_id'], data[i]['author'], data[i]['date']])

'''
Extracs data for map + reduce script FreqRessort.py
'''
def createDataForFreqRessort():
    data = dbc.collectionTazData.find()
    amountOfData = data.count()
    with open('data/freqRessorts.data', mode='w', encoding='utf-8') as employee_file:
        for i in range(0, amountOfData):
            writer = csv.writer(employee_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([data[i]['_id'], data[i]['ressort'], data[i]['date']])

'''
Transform data to dataframe
IN: collection = collection of json files from mongodb
OUT: df = collection as dataframe
'''
def transformDataToDf(collection):
    data = collection.find()
    df = pd.DataFrame.from_dict(data)
    return df

'''
Find substring between substrings 
IN: s = string for finding substring, first = first character for beginning of substring, last = last character for ending of substring
OUT: substring
'''
def find_between(s,first,last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

'''
Add ressorts to focusdatabase
IN: collectionFocus = collection from focus
'''
def addRessortsToFocusDatabase(collectionFocus):
    data = collectionFocus.find()
    amountOfData = data.count()
    df = transformDataToDf(collectionFocus)
    for i in range(0, amountOfData):
        entity = data[i]
        url = df.at[i, '_id']
        suburl = url[21:]
        ressort = find_between(suburl, '/', '/')
        entity['ressort'] = ressort
        collectionFocus.save(entity)
        print(entity)

'''
Get bodys of collection
IN: collection = collection of json files from mongodb
OUT: listOfBodys = list of all bodys 
'''
def getBodys(collection):
    listOfBodys = []
    data = collection.find()
    amountOfData = data.count()
    df = transformDataToDf(collection)
    for i in range(0, amountOfData):
            listOfBodys.append(df.at[i, 'body'])
    return listOfBodys

'''
Analyzes the number of articles grouped by author and ressort
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
OUT: dfNumberOfArticlesGroupedByAuthorAndRessort = dataframe with number of articles grouped by author and ressort
'''
def getNumberOfArticlesGroupedByAuthorAndRessort(dfTazClean):
    dfNumberOfArticlesGroupedByAuthorAndRessort = dfTazClean.groupby(['author', 'ressort']).count().sort_values(by=['_id'])

    return dfNumberOfArticlesGroupedByAuthorAndRessort

'''
Analyzes the number of articles grouped by author and ressort
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
OUT: dfNumberOfArticlesGroupedByAuthorAndRessort = dataframe with number of articles grouped by author and ressort
'''
def getNumberOfArticlesGroupedByRessort(dfTazClean):
    dfNumberOfArticlesGroupedByRessort = dfTazClean.groupby(['ressort']).count().sort_values(by=['_id'])

    return dfNumberOfArticlesGroupedByRessort

'''
Analyzes the largest value of a column from a dataframe
IN: df = dataframe
OUT: highestValueDfByColumn = highest value of a column from a dataframe 
'''
def getLargestValuesByColumn(df, amount, column):
    highestValueDfByColumn = df.nlargest(amount, column)

    return highestValueDfByColumn

'''
Generates plot for number of articles for authors in ressorts
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
'''
def getPlotForNumberOfArticlesForAuthorsInRessorts(dfTazClean, ressort):
    dfTazCleanForRessort = dfTazClean[dfTazClean.ressort == ressort]
    authorsInRessort = dfTazCleanForRessort['author'].unique()

    freqAuthorInRessort = []
    j = 0

    for i in range (0, len(authorsInRessort)):
        j = dfTazCleanForRessort.loc[dfTazCleanForRessort.author == authorsInRessort[i], 'author'].count()
        freqAuthorInRessort.append(j)
        j = 0

    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(freqAuthorInRessort))

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))

    ax.barh(y_pos, freqAuthorInRessort, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(authorsInRessort)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Anzahl Artikel')
    ax.set_title('Ressort ' + ressort)
    fig.show()
    fig.savefig('data/numberOfArticlesForAuthorsInRessort_' + ressort + '.svg')

'''
Analyzes the number of articles grouped by dates
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
OUT: dfNumberOfArticlesGroupedByDate = dataframe with number of articles grouped by dates
'''
def getNumberOfArticlesGroupedByDates(dfTazClean):
    dfNumberOfArticlesGroupedByDate = dfTazClean.groupby('date').count().sort_values(by=['_id'])
    return dfNumberOfArticlesGroupedByDate

'''
Analyzes the number of articles grouped by ressort and dates
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
OUT: dfNumberOfArticlesGroupedByRessortAndDate = dataframe with number of articles grouped by ressort and date
'''
def getNumberOfArticlesgroupedByRessortAndDate(dfTazClean):
    dfNumberOfArticlesGroupedByRessortAndDate = dfTazClean.groupby(['ressort', 'date']).count().sort_values(by=['_id'])
    return dfNumberOfArticlesGroupedByRessortAndDate

'''
Analyzes the number of keywords mentioned in taz
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
OUT: dfNumberOfAllKeywords = dataframe with number of keywords mentioned in taz
'''
def getNumberOfAllKeywords(dfTazClean):
    dfTazCleanKeywords = dfTazClean.keywords

    keywordsData = []
    amountKeywords = []
    for i in range (0, len(dfTazCleanKeywords)):
        t = dfTazCleanKeywords[i]
        for j in range (0, len(t)):
            keywordsData.append(t[j])
            amountKeywords.append(1)
    print(keywordsData)
    print(amountKeywords)
    data = {'Keyword': keywordsData,
            'Amount': amountKeywords
    }

    df = pd.DataFrame(data, columns=['Keyword', 'Amount'])
    dfNumberOfAllKeywords = df.groupby('Keyword').count().sort_values(by=['Amount'])

    return dfNumberOfAllKeywords

'''
Defines to which category a value is assigned within the contingency table
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
OUT: categorie = categorie of the contingency table which depends on categories and the value
'''
def defineContingencyCategorie(value, categories):
    if value < categories[0][1]:
        return categories[0][0]
    elif value < categories[1][1]:
        return categories[1][0]
    elif value < categories[2][1]:
        return categories[2][0]
    elif value >= categories[2][1]:
        return categories[3][0]

'''
Structures ressorts in dataframe
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors
    substituteList = list containing rules for the substitution of ressorts
    deleteList = list containing ressorts which should be delteted
OUT: structuredDfTazClean = structured dataframe which depends on given rules (list)
'''
def structureRessortsInDf(dfTazClean, substituteList, deleteList):
    for i in range(0, len(substituteList)):
        dfTazClean['ressort'] = dfTazClean['ressort'].replace([substituteList[i][0]],
                                                              substituteList[i][1])
    #    df['column name'] = df['column name'].replace(['old value'], 'new value')

    for i in range(0, len(deleteList)):
        dfTazClean = dfTazClean[dfTazClean.ressort != deleteList[i]]

    structuredDfTazClean = dfTazClean
    return structuredDfTazClean

'''
Create crosstab, calculate chi square and create contingency table
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
IN: structuredDfTazClean = structured dataframe
'''
def chi2ConintengencyAnalysis(structuredDfTazClean):
    ressortData = []
    numberOfWordsData = []
    for index, row in structuredDfTazClean.iterrows():
        ressortData.append(row['ressort'])
        numberOfWordsData.append(len(str(row['body']).split()))

    categories = []
    for i in range(0, len(numberOfWordsData)):
        categorie = defineContingencyCategorie(numberOfWordsData[i], contingencyCategories)
        categories.append(categorie)

    data = {'ressort': ressortData,
            'numberOfWords': numberOfWordsData,
            'categorie': categories}

    df = pd.DataFrame(data, columns=['ressort', 'numberOfWords', 'categorie'])

    crosstab = pd.crosstab(df['ressort'], df['categorie'])
    print(crosstab)
    print("\n")

    observedValues = crosstab.values

    chi2_stat, p_val, dof, ex = stats.chi2_contingency(observedValues)

    print("===Chi2 Stat===")
    print(chi2_stat)
    print("\n")
    print("===Degrees of Freedom===")
    print(dof)
    print("\n")
    print("===P-Value===")
    print(p_val)
    print("\n")
    print("===Contingency Table===")
    print(ex)

'''
Performs a anova anlyses based on number of words for 4 different ressorts
IN: structuredDfTazClean = structured dataframe
    ressort1 = name of the first to be considered ressort (string)
    ressort2 = name of the second to be considered ressort (string)
    ressort3 = name of the third to be considered ressort (string)
    ressort4 = name of the fourth to be considered ressort (string)
'''
def anovaAnalysisNumberOfWordsFor4Ressorts(structuredDfTazClean, ressort1, ressort2, ressort3, ressort4):
    numberOfWordsRessort1 = []
    numberOfWordsRessort2 = []
    numberOfWordsRessort3 = []
    numberOfWordsRessort4 = []

    for index, row in structuredDfTazClean.iterrows():
        if row['ressort'] == ressort1:
            numberOfWordsRessort1.append(len(str(row['body']).split()))
        elif row['ressort'] == ressort2:
            numberOfWordsRessort2.append(len(str(row['body']).split()))
        elif row['ressort'] == ressort3:
            numberOfWordsRessort3.append(len(str(row['body']).split()))
        elif row['ressort'] == ressort4:
            numberOfWordsRessort4.append(len(str(row['body']).split()))

    fOneWay = f_oneway(numberOfWordsRessort1, numberOfWordsRessort2, numberOfWordsRessort3, numberOfWordsRessort4)
    return fOneWay

'''
Get the number of unique authors
IN: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors
OUT: numberOfUniqueAuthors = number of unique authors
'''
def getNumberOfUniqueAuthors(dfTazClean):
    numberOfUniqueAuthors = dfTazClean['author'].nunique()
    return numberOfUniqueAuthors

'''
Performs and plot a regression analysis for a timeseries (number of articles) of a month
https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
IN: excelsheet = name of the excelsheet incl. file extension which contains the timeseries
'''
def plotRegressionAnalysisForTimeSeries(excelSheet):
    timeSeries = pd.read_excel(excelSheet)

    month = excelSheet[16:18]

    x = pd.DataFrame(timeSeries['day'])
    y = pd.DataFrame(timeSeries['amount'])

    model = LinearRegression()
    model.fit(x, y)

    intercept = model.intercept_[0]
    slope = model.coef_[0, 0]
    r_sq = model.score(x, y)
    print("intercept:", intercept)
    print("slope:", slope)
    print("coefficient of determination:", r_sq)

    plt.scatter(timeSeries['day'], timeSeries['amount'], alpha=0.7)
    plt.title('Regressionsanalyse - Anzahl der Artikel nach Tagen - ' + month +'/2020 (TAZ)')
    plt.xlabel("Tag")
    plt.ylabel("Anzahl der Artikel")

    t = np.array([min(x.loc[:, 'day']), max(x.loc[:, 'day'])])
    t = t.reshape(-1, 1)
    plt.plot(t, model.predict(t), "-r")
    plt.savefig('data/regressionAnalysis_timeSeries_' + month + '_2020.svg')
    plt.show()

def main():

    cleanDfTaz = dc.cleanTazMetaData(dbc.collectionTazData)

    #create data for map + reduce use-cases
    createDataForFreqAuthor()
    createDataForFreqRessort()

    #print number of unique auhtors
    print('Number of unique authors: ', getNumberOfUniqueAuthors(cleanDfTaz))

    #csv top 20 number of articles grouped by author and ressort
    groupedByAuthorAndRessortDfTaz = getNumberOfArticlesGroupedByAuthorAndRessort(cleanDfTaz)
    highestGroupedByAuthorAndRessortDfTaz = getLargestValuesByColumn(groupedByAuthorAndRessortDfTaz, 20, '_id')
    highestGroupedByAuthorAndRessortDfTaz.to_csv('data/top20_numberOfArticlesGroupedByAuthorAndRessort.csv')

    #csv top 30 number of articles grouped by ressort
    groupedByRessortDfTaz = getNumberOfArticlesGroupedByRessort(cleanDfTaz)
    highestGroupedByRessortDfTaz = getLargestValuesByColumn(groupedByRessortDfTaz, 30, '_id')
    highestGroupedByRessortDfTaz.to_csv('data/top30_numberOfArticlesGroupedByRessort.csv')

    #plots number of articles for authors in ressorts -> sustainable ressorts
    for i in range(0, len(sustainabilityRessortsTaz)):
        plotNumberOfArticlesForAuthorsInRessort = getPlotForNumberOfArticlesForAuthorsInRessorts(cleanDfTaz, sustainabilityRessortsTaz[i])

    #plots number of articles for authors in ressorts -> not sustainabale ressorts
    for i in range(0, len(notSustainabilityRessortsTaz)):
        plotNumberOfArticlesForAuthorsInRessort = getPlotForNumberOfArticlesForAuthorsInRessorts(cleanDfTaz, notSustainabilityRessortsTaz[i])

    #csv number of all articles for dates
    numberOfArticlesForDates = getNumberOfArticlesGroupedByDates(cleanDfTaz)
    numberOfArticlesForDates.to_csv('data/numberOfArticlesForDates.csv')

    #csv number of all articles for dates in ressorts
    numberOfArticlesForDatesInRessorts = getNumberOfArticlesgroupedByRessortAndDate(cleanDfTaz)
    numberOfArticlesForDatesInRessorts.to_csv('data/numberOfArticlesForDatesInRessorts.csv')

    #csv number of all keywords mentioned in taz
    numberOfAllKeywords = getNumberOfAllKeywords(cleanDfTaz)
    numberOfAllKeywords.to_csv('data/numberOfAllKeywords.csv')

    #anova analysis -> numberOfWords in main ressorts
    df = structureRessortsInDf(cleanDfTaz, mainRessortsWithSubressort, secondaryRessortsWithSubressorts)
    fOneWay = anovaAnalysisNumberOfWordsFor4Ressorts(df, 'Oeko', 'Politik', 'Kultur', 'Gesellschaft')
    print(fOneWay)

    '''
    plots regression analysis -> number of articles for month
    !!! perform separate
    '''
    plotRegressionAnalysisForTimeSeries('data/timeSeries_11.xls')
    plotRegressionAnalysisForTimeSeries('data/timeSeries_12.xls')

    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', 2):  # more options can be specified also
       print(df)
    '''

if __name__ == '__main__':
        main()
