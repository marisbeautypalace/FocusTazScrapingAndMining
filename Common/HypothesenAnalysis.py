import math
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from Common import DatabaseConnection as dbc
from Common import DataCleaning as dc

#most similar words to UN sustainablity goals
#list containing poverty sustainability goals
Poverty = ['Armut',
           'Arbeitslosigkeit',
           'Hunger',
           'Ungleichheit',
           'Elend',
           'soziale Ausgrenzung',
           'Ungerechtigkeit',
           'soziale Ungleichheit',
           'Analphabetismus',
           'soziale Ungerechtigkeit']

#list containing hunger sustainability goals
Hunger = ['Hunger',
          'Durst',
          'Hungers',
          'Heisshunger',
          'stillt',
          'Hunger leiden',
          'Armut',
          'hungert']

#list containing health sustainability goals
Health = ['Gesundheit',
          'Wohlbefinden',
          'Ernaehrung',
          'Ernährung',
          'Umwelt',
          'psychische Gesundheit',
          'Bildung',
          'gesunde Lebensweise',
          'Nahrungsmittelsicherheit']

#list containing education sustainability goals
Education = ['Bildung',
             'leistbares Wohnen',
             'bezahlbare Mieten',
             'soziale Teilhabe',
             'fruehkindliche Bildung',
             'frühkindliche Bildung',
             'Soziales',
             'Integration',
             'Bildungsgerechtigkeit',
             'Teilhabe',
             'leistbares']

#list containing equality sustainability goals
Equality = ['Gleichstellung',
            'Gleichberechtigung',
            'Oeffnung Ehe',
            'Öffnung Ehe',
            'volle Gleichstellung',
            'Lebenspartnerschaften',
            'Ehe',
            'Adoptionsrecht',
            'homosexuelle Partnerschaft',
            'Chancengleichheit',
            'Gleichbehandlung',
            'gleiche Bezahlung']

#list containing drinkingwater sustainability goals
DrinkingWater = ['Trinkwasser',
                 'Leitungswasser',
                 'Abwasser',
                 'Frischwasser',
                 'Trinkwasserversorgung',
                 'Grundwasser',
                 'gechlort',
                 'sauberes Wasser',
                 'Fremdwasser',
                 'Wasser']

#list containing energytransition sustainability goals
EnergyTransition = ['Energiewende',
                    'Energiepolitik',
                    'Umsetzung Energiewende',
                    'erneuerbare Energien',
                    'Netzausbau',
                    'Klimaschutz',
                    'erneuerbar',
                    'Atomausstieg',
                    'ökologische Modernisierung']

#list containing economicgrowth sustainability goals
EconomicGrowth = ['Wirtschaftswachstum',
                  'Wachstum',
                  'Binnennachfrage',
                  'Wirtschaftsentwicklung',
                  'Exportwachstum',
                  'Kreditwachstum',
                  'BIP-Wachstum',
                  'privaten Konsum',
                  'Bruttoinlandsprodukt',
                  'zweitgrössten Volkswirtschaft']

#list containing infrastructue sustainability goals
Infrastructur = ['Infrastruktur',
                 'Verkehrsinfrastruktur',
                 'Infrastrukturen',
                 'marode Infrastruktur',
                 'Verkehrswege',
                 'Verkehrs-Infrastruktur',
                 'Investitionen',
                 'Kitas',
                 'Ganztagsschulen',
                 'Gesundheitsversorgung',
                 'Strassen',
                 'Straßen',
                 'Brücken',
                 'Bruecken',
                 'Investitionen']

#list containing inequality sustainability goals
Inequality = ['Ungleichheit',
              'Ungleichheiten',
              'Einkommensungleichheit',
              'soziale Ungleichheit',
              'Einkommensunterschiede',
              'Armut',
              'soziale Spaltung',
              'wachsende Kluft',
              'Spaltung Gesellschaft',
              'Arm Reich',
              'Einkommensschere']

#list containing city sustainability goals
City = ['Stadt',
        'Kommune',
        'Gemeinde',
        'Kreisstadt',
        'Stadtverwaltung',
        'Nachbarstadt',
        'Städte',
        'Kreises',
        'Landkreis',
        'Landeshauptstadt']

#list containing consumerbehavior sustainability goals
ConsumerBehavior = ['Konsumverhalten',
                    'Kaufverhalten',
                    'Konsumgewohnheiten',
                    'Einkaufsverhalten',
                    'Verbraucherverhalten',
                    'Freizeitverhalten',
                    'Mobilitätsverhalten',
                    'Gesundheitsbewusstsein',
                    'Ernaehrungsgewohnheiten',
                    'Reiseverhalten',
                    'Trinkverhalten']

#list containing climatechange sustainability goals
ClimateChange = ['Klimaschutz',
                 'Umweltschutz',
                 'Umwelt',
                 'Klimaschutz',
                 'Energiesparen',
                 'erneuerbare Energien',
                 'Klima',
                 'Umweltpolitik',
                 'Energiepolitik',
                 'Energieeffizienz',
                 'alternative Energien']

#list containing sea sustainability goals
Sea = ['Meer',
       'Ozean',
       'Strand',
       'See',
       'Bucht',
       'Nordsee',
       'Küste',
       'Kueste',
       'Atlantik',
       'Mittelmeer',
       'Brandung',
       'Ostsee']

#list containing habitat sustainability goals
Habitat = ['Lebensraum',
           'Lebensräume',
           'Artenvielfalt',
           'Pflanzen',
           'Tierarten',
           'Artenreichtum',
           'idealen Lebensraum',
           'Pflanzenarten',
           'seltene Arten',
           'Biotope',
           'Wiesenvoegel']

#list containing peace sustainability goals
Peace = ['Frieden',
         'Friede',
         'Weltfrieden',
         'Frieden Palaestinensern',
         'Versöhnung',
         'Gerechtigkeit',
         'dauerhafter Frieden',
         'geeintes Europa',
         'inneren Frieden'
]

#list containing different sustainability goals
SustainabilityGoals = [Poverty,
                       Hunger,
                       Health,
                       Education,
                       Equality,
                       DrinkingWater,
                       EnergyTransition,
                       EconomicGrowth,
                       Infrastructur,
                       Inequality,
                       City,
                       ConsumerBehavior,
                       ClimateChange,
                       Sea,
                       Habitat,
                       Peace]

#list of most similar words to 'sustainability' from the german model from nlp project
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

#list of csv files from nlp project which contains polarity and subjectivity of each article separated according to sustainability articles and not sustainability articles
NlpAnalysis = ['TazSustainability.csv',
               'TazNotSustainability.csv',
               'FocusSustainability.csv',
               'FocusNotSustainability.csv'
               ]

'''
Get number of bodys which contains a hitword from a list
IN: df = dataframe of a collection (json files from mongodb)
    list = list of hitwords whose frequency is counted
OUT: numberOfBodysWhichContainsHitword = number of bodys which contains a hitword from a list
'''
def getNumberOfHitsForWordsInBody(df, hitwords):
    numberOfBodysWhichContainsHitword = 0
    dfBody = df.body
    for i in range(0, dfBody.size):
        contains = False
        bodyToInvestigate = str(dfBody[i])
        for j in range(0, len(hitwords)):
            if hitwords[j] in bodyToInvestigate:
                contains = True
        if contains:
            numberOfBodysWhichContainsHitword += 1
    return numberOfBodysWhichContainsHitword

'''
Get number of words in the bodys of a newspaper
IN: df = dataframe of a collection (json files from mongodb)
OUT: allNumberOfWords = number of words in the bodys of a newspaper
'''
def getNumberOfWordsForBodys(df):
    dfBody = df.body
    allNumberOfWords = 0
    for i in range(0, dfBody.size):
        numberOfWords = len(str(dfBody[i]).split())
        allNumberOfWords += numberOfWords
    return allNumberOfWords

'''
Get number of words in the bodys of a newspaper for every article
IN: df = dataframe of a collection (json files from mongodb)
OUT: numberOfWordsArticle = list of number of words in the bodys of a newspaper for every article
'''
def getNumberOfWordsForBodysForEveryArticle(df):
    dfBody = df.body
    numberOfWordsArticle = []
    for i in range(0, dfBody.size):
        numberOfWords = 0
        numberOfWords = len(str(dfBody[i]).split())
        numberOfWordsArticle.append(numberOfWords)
    return numberOfWordsArticle

'''
Get number of hitwords in bodys of a newspaper
IN: df = dataframe of a collection (json files from mongodb)
    list = list of hitwords whose frequency is counted
OUT: allNumberOfWords = number of hitwords in bodys of a newspaper
'''
def getNumberOfHitwordsForBodys(df, hitwords):
    dfBody = df.body
    allNumberOfWords = 0
    contains = False
    for i in range(0, dfBody.size):
        bodyToInvestigate = str(dfBody[i])
        for j in range(0, len(hitwords)):
            if hitwords[j] in bodyToInvestigate:
                contains = True
        if contains:
            allNumberOfWords += len(bodyToInvestigate.split())
            contains = False
    return allNumberOfWords

'''
Get number of hitwords in bodys of a newspaper for every article
IN: df = dataframe of a collection (json files from mongodb)
    list = list of hitwords whose frequency is counted
OUT: numberOfWordsArticle = number of hitwords in bodys of a newspaper for every article
'''
def getListNumberOfHitwordsForBodysForEveryArticle(df, hitwords):
    dfBody = df.body
    numberOfWords = 0
    numberOfWordsArticle = []
    contains = False
    for i in range(0, dfBody.size):
        bodyToInvestigate = str(dfBody[i])
        for j in range(0, len(hitwords)):
            if hitwords[j] in bodyToInvestigate:
                contains = True
        if contains:
            numberOfWords = len(bodyToInvestigate.split())
            numberOfWordsArticle.append(numberOfWords)
            contains = False
    return numberOfWordsArticle

'''
Get number of not hitwords in bodys of a newspaper for every article
IN: df = dataframe of a collection (json files from mongodb)
    list = list of hitwords whose frequency is not relevant
OUT: numberOfWordsArticleNotHitwords = number of not hitwords in bodys of a newspaper for every article
'''
def getListNumberOfNotHitwordsForBodysForEveryArticle(df, hitwords):
    dfBody = df.body
    numberOfWords = 0
    numberOfWordsArticleNotHitwords = []
    contains = False
    for i in range(0, dfBody.size):
        bodyToInvestigate = str(dfBody[i])
        for j in range(0, len(hitwords)):
            if hitwords[j] in bodyToInvestigate:
                contains = True
        if not contains:
            numberOfWords = len(bodyToInvestigate.split())
            numberOfWordsArticleNotHitwords.append(numberOfWords)
        contains = False
    return numberOfWordsArticleNotHitwords

'''
Get the body of an article with a specific length
IN: df = dataframe of a collection (json files from mongodb)
    value = length of the article
OUT: listOfIds = list of ids which matches with specific length
'''
def getArticleIdForSpecificLength(df, value):
    dfBody = df.body
    dfId = df._id
    listOfIds = []
    for i in range(0, dfBody.size):
        numberOfWords = len(str(dfBody[i]).split())
        if numberOfWords == value:
            listOfIds.append(dfId[i])
    return listOfIds

'''
Get the body of an article without body
IN: df = dataframe of a collection (json files from mongodb)
OUT: listOfIds = list of ids whitout bodys
'''
def getArticleIdForNaN(df):
    dfBody = df.body
    dfId = df._id
    listOfIds = []
    for i in range(0, dfBody.size):
        numberOfWords = len(str(dfBody[i]).split())
        if math.isnan(numberOfWords):
            listOfIds.append(dfId[i])
    return listOfIds

'''
Performs a two sample independent ttest
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
IN: distributionA = distribution of variable a
    distributionB = distribution of variable b
'''
def tTestTwoSampleIndependent(distributionA, distributionB):
    t2, p2 = stats.ttest_ind(distributionA, distributionB)
    print("t = " + str(t2))
    print("p = " + str(p2))

'''
Performs a one sample ttest
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
IN: distributionA = distribution of variable a
    expectedMean = expected mean value of the distribution
'''
def tTestOneSample(distributionA, expectedMean):
    t2, p2 = stats.ttest_1samp(distributionA, expectedMean)
    print("t = " + str(t2))
    print("p = " + str(p2))

'''
Analyses the hardfacts for a newspaper
IN: df = dataframe of a collection (json files from mongodb)
OUT: structuredDfTazClean = structured dataframe which depends on given rules (list)
'''
def analyseHardfacts(df):
    print('Number of articles: ', len(df))
    numberOfWords = getNumberOfWordsForBodysForEveryArticle(df)
    print('Number of words: ', sum(numberOfWords))
    print('Mean words of an article: ', np.mean(numberOfWords))
    print('Standard deviation words of an article: ', np.std(numberOfWords))
    print('Minimum words of an article: ', min(numberOfWords))
    print('Maximum words of an article: ', max(numberOfWords))

    hitsSustainabilityGoalsInBodfOfNewspaper = 0
    for i in range(0, len(SustainabilityGoals)):
        count = getNumberOfHitsForWordsInBody(df, SustainabilityGoals[i])
        hitsSustainabilityGoalsInBodfOfNewspaper += count
    print('Number of hitwords for sustainability goals: ', hitsSustainabilityGoalsInBodfOfNewspaper)

    hitsMostSimilarWordsSustainabilityGermanModel = getNumberOfHitsForWordsInBody(df, MostSimilarWordsSustainabilityGermanModel)
    print('Number of hitwords for most similiar words sustainabitlity german model: ', hitsMostSimilarWordsSustainabilityGermanModel)


'''
Plots a boxplot regarding the number of words for both newspaper
IN: numberOfWordsTaz = list with number of words of every article for taz
    numberOfWordsFocus = list with number of words of every article for focus
'''
def plotBoxplotNumberOfWordsForAllNewspaper(numberOfWordsTaz, numberOfWordsFocus):

    numberOfWordsNewspaper = numberOfWordsTaz + numberOfWordsFocus

    allocationNumberOfWordsToNewspaper = []
    for i in range(0, len(numberOfWordsTaz)):
        allocationNumberOfWordsToNewspaper.append('TAZ')
    for i in range(0, len(numberOfWordsFocus)):
        allocationNumberOfWordsToNewspaper.append('FOCUS')

    df = pd.DataFrame({'Zeitung': allocationNumberOfWordsToNewspaper,
                       'Anzahl der Wörter': numberOfWordsNewspaper})

    boxplot = df.boxplot(column=['Anzahl der Wörter'], by="Zeitung")
    boxplot.plot()
    plt.title('Anzahl der Wörter')
    plt.suptitle('')
    plt.savefig('data/boxplotNumberOfWordsForAllNewspaper.svg')
    plt.show()

'''
Plots a boxplot regarding the number of words for one newspaper
IN: numberOfWords = list with number of words of every article for 
    nameNewspaper = name of the newspaper either taz or focus
'''
def plotBoxplotNumberOfWordsForOneNewspaper(numberOfWords, nameNewspaper):

    allocationNumberOfWordsToNewspaper = []
    for i in range(0, len(numberOfWords)):
        allocationNumberOfWordsToNewspaper.append(nameNewspaper)

    df = pd.DataFrame({'Zeitung': allocationNumberOfWordsToNewspaper,
                       'Anzahl der Wörter': numberOfWords})

    boxplot = df.boxplot(column=['Anzahl der Wörter'], by="Zeitung")
    boxplot.plot()
    plt.title('Anzahl der Wörter ' + nameNewspaper)
    plt.suptitle('')
    plt.savefig('data/boxplotNumberOfWordsFor_' + nameNewspaper + '.svg')
    plt.show()

'''
Performs a analysis of polarity and subjectivity from nlp for every article -> mean, std, df and one sample ttests
IN: csvList = ['TazSustainability.csv', -> taz articles regarding sustainability
               'TazNotSustainability.csv', -> taz articles regarding not sustainability
               'FocusSustainability.csv', -> focus articles regarding sustainability
               'FocusNotSustainability.csv'] -> focs articles regarding not sustainability
'''
def nlpAnalysisRegardingPolarityAndSubjectivity(csvList):
    for i in range(0, len(csvList)):
        print(csvList[i])
        dfNlpAnalysis = pd.read_csv('data/' + csvList[i])

        polarity = []
        subjectivity = []
        for index, row in dfNlpAnalysis.iterrows():
            polarity.append(row['0'])
            subjectivity.append((row['1']))

        print('mean polarity: ', np.mean(polarity))
        print('std polarity: ', np.std(polarity))
        print('mean subjectivity: ', np.mean(subjectivity))
        print('std subjectivity: ', np.std(subjectivity))
        print('df: ', len(polarity) - 1)

        #one sample independent ttests for polarity and subjectivity with expected mean value
        print('one sample independent ttest polarity:')
        tTestOneSample(polarity, 0)
        print("\n")
        print('one sample independent ttest subjectivity:')
        tTestOneSample(subjectivity, 0.5)

        print("\n")

'''
Performs a analysis of subjectivity from nlp for every article -> two sample ttest for sustainability against not sustainability 
IN: csvList = ['TazSustainability.csv', -> taz articles regarding sustainability
               'TazNotSustainability.csv', -> taz articles regarding not sustainability
               'FocusSustainability.csv', -> focus articles regarding sustainability
               'FocusNotSustainability.csv'] -> focs articles regarding not sustainability
'''
def nlpAnalysisRegardingSubjectivity(csvList):

    dfTazSustainability = pd.read_csv('data/' + csvList[0], usecols=['1'])
    dfTazNotSustainability = pd.read_csv('data/' + csvList[1], usecols=['1'])
    dfFocusSustainability = pd.read_csv('data/' + csvList[2], usecols=['1'])
    dfFocusNotSustainability = pd.read_csv('data/' + csvList[3], usecols=['1'])

    dfSubjectivity = pd.concat([dfTazSustainability, dfTazNotSustainability, dfFocusSustainability, dfFocusNotSustainability], axis=1)
    dfSubjectivity.columns = ['TazSustainabilitySubjectivity', 'TazNotSustainabilitySubjectivity', 'FocusSustainabilitySubjectivity', 'FocusNotSustainabilitySubjectivity']

    subjectivityTazSustainability = dfSubjectivity['TazSustainabilitySubjectivity'].tolist()
    cleanedSubjectivityTazSustainability = [x for x in subjectivityTazSustainability if ~np.isnan(x)]
    subjectivityTazNotSustainability = dfSubjectivity['TazNotSustainabilitySubjectivity'].tolist()
    cleanedSubjectivityTazNotSustainability = [x for x in subjectivityTazNotSustainability if ~np.isnan(x)]
    subjectivityFocusSustainability = dfSubjectivity['FocusSustainabilitySubjectivity'].tolist()
    cleanedSubjectivityFocusSustainability = [x for x in subjectivityFocusSustainability if ~np.isnan(x)]
    subjectivityFocusNotSustainability = dfSubjectivity['FocusNotSustainabilitySubjectivity'].tolist()
    cleanedSubjectivityFocusNotSustainability = [x for x in subjectivityFocusNotSustainability if ~np.isnan(x)]

    print('one sample independent ttest subjectivity for taz:')
    tTestTwoSampleIndependent(cleanedSubjectivityTazSustainability, cleanedSubjectivityTazNotSustainability)

    print("\n")
    print('one sample independent ttest subjectivity for focus:')
    tTestTwoSampleIndependent(cleanedSubjectivityFocusSustainability, cleanedSubjectivityFocusNotSustainability)

    print("\n")

'''
Calculates chi square for number of words regarding sustainability goals
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
IN: df = dataframe of a collection (json files from mongodb)
OUT: chiSquare = chisquare value
'''
def calculateChiSquare(df):
    hitsSustainabilityGoalsInBodyfOfNewspaper = []
    for i in range(0, len(SustainabilityGoals)):
        count = getNumberOfHitsForWordsInBody(df, SustainabilityGoals[i])
        hitsSustainabilityGoalsInBodyfOfNewspaper.append(count)

    sumHitsSustainabilityGoalsInBodfOfNewspaper = sum(hitsSustainabilityGoalsInBodyfOfNewspaper)
    expectedMeanHitsSustainabilityGoalsInBodfOfNewspaper = sumHitsSustainabilityGoalsInBodfOfNewspaper / len(hitsSustainabilityGoalsInBodyfOfNewspaper)
    listOfExpectedMeanHitsSustainabilityGoalsInBodfOfNewspaper = []
    for i in range(0, len(hitsSustainabilityGoalsInBodyfOfNewspaper)):
        listOfExpectedMeanHitsSustainabilityGoalsInBodfOfNewspaper.append(expectedMeanHitsSustainabilityGoalsInBodfOfNewspaper)

    chiSquare, p = stats.chisquare(hitsSustainabilityGoalsInBodyfOfNewspaper, listOfExpectedMeanHitsSustainabilityGoalsInBodfOfNewspaper)

    return chiSquare, p

def main():
    cleanDfTaz = dc.cleanTazMetaData(dbc.collectionTazData)
    dfFocus = dc.transformDataToDf(dbc.collectionFocusData)

    #print hardfacts for taz and focus
    print('TAZ:')
    analyseHardfacts(cleanDfTaz)
    print("\n")
    print('FOCUS:')
    analyseHardfacts(dfFocus)

    #further investigations of min and max value FOCUS
    print(getArticleIdForSpecificLength(dfFocus, 0))
    print(getArticleIdForSpecificLength(dfFocus, 10812))

    #two sample independent ttest for number of words in both newspaper
    numberOfWordsTaz = (getNumberOfWordsForBodysForEveryArticle(cleanDfTaz))
    numberOfWordsFocus = (getNumberOfWordsForBodysForEveryArticle(dfFocus))
    print('two sample independent ttest for number of words in both newspaper:')
    tTestTwoSampleIndependent(numberOfWordsTaz, numberOfWordsFocus)

    #two sample independent ttest for number of sustainability hitwords and number of not words without sustainability hitwords -> TAZ
    numberOfHitwordsSustainabilityTaz = getListNumberOfHitwordsForBodysForEveryArticle(cleanDfTaz, MostSimilarWordsSustainabilityGermanModel)
    numberOfWordsTazWithoutSustainabilityHitwordsTaz = getListNumberOfNotHitwordsForBodysForEveryArticle(cleanDfTaz, MostSimilarWordsSustainabilityGermanModel)
    print('two sample independent ttest for number of sustainability hitwords and number of not words without sustainability hitwords -> TAZ:')
    tTestTwoSampleIndependent(numberOfHitwordsSustainabilityTaz, numberOfWordsTazWithoutSustainabilityHitwordsTaz)

    #two sample independent ttest for number of sustainability hitwords and number of not words without sustainability hitwords -> FOCUS
    numberOfHitwordsSustainabilityFocus = getListNumberOfHitwordsForBodysForEveryArticle(dfFocus, MostSimilarWordsSustainabilityGermanModel)
    numberOfWordsTazWithoutSustainabilityHitwordsFocus = getListNumberOfNotHitwordsForBodysForEveryArticle(dfFocus, MostSimilarWordsSustainabilityGermanModel)
    print('two sample independent ttest for number of sustainability hitwords and number of not words without sustainability hitwords -> FOCUS:')
    tTestTwoSampleIndependent(numberOfHitwordsSustainabilityFocus, numberOfWordsTazWithoutSustainabilityHitwordsFocus)

    #deep analysis of the polarity and subjectivity from nlp -> mean, std, df and two sample independent ttests
    nlpAnalysisRegardingPolarityAndSubjectivity(NlpAnalysis)

    #twosample ttest for subjectivity from nlp -> sustainability against not sustainability
    nlpAnalysisRegardingSubjectivity(NlpAnalysis)

    #plots boxplots for number of words
    plotBoxplotNumberOfWordsForAllNewspaper(numberOfWordsTaz, numberOfWordsFocus)
    plotBoxplotNumberOfWordsForOneNewspaper(numberOfWordsTaz, 'TAZ')
    plotBoxplotNumberOfWordsForOneNewspaper(numberOfWordsFocus, 'FOCUS')

    #calculate chi square for number of words regarding sustainability goals
    chi2Taz = calculateChiSquare(cleanDfTaz)
    chi2Focus = calculateChiSquare(dfFocus)
    print('chi2Taz: ', chi2Taz)
    print('chi2Focus: ', chi2Focus)

    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', 3):  # more options can be specified also
       print(df)
    '''

if __name__ == '__main__':
    main()

