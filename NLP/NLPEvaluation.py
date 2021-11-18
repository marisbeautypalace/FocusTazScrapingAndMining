from NLP.SpeachAnalysis import NLPObject
from NLP.Common import DatabaseConnection as dbc
import NLP.Common.DataOperations as do



bodysFocus = do.getBodys(dbc.collectionFocusData)
bodysTaz = do.getBodys(dbc.collectionTazData)
bodysAll = bodysFocus + bodysTaz

#rawCorpus = []

wordList = ['nachhaltigkeit', 'armut', 'hunger', 'gesunheit' , 'bildung', 'gleichheit', 'gleichstellung', 'trinkwasser', 'energie', 'energiewende', 'menschenwürde',
            'infrastruktur', 'ungleichheit', 'stadtenwicklung','konsum', 'konsumverhalten', 'klimaschutz', 'ökosysteme', 'frieden', 'partnerschaft', 'wirtschaftswachstum',
            'stadt', 'meer', 'lebensraum','wirtschaften', 'ökologie', 'regionalität', 'umweltschutz', 'energieeffizienz', 'ressourcenschonung', 'ressourceneffizienz',
            'wohlergehen', 'meeresschutz', 'frieden', 'global', 'trinkwasser', 'energiewende', 'stadtentwicklung']

NLP = NLPObject()

processedCorpusFocus = NLP.processCorpus(bodysFocus)
processedCorpusTaz = NLP.processCorpus(bodysTaz)
processedCorpusAll = NLP.processCorpus(bodysAll)

file1 = open('data/WordFrequencies.txt', 'w')

'''Count word frequencies in a Corpus and write them into the WordFrequencies text file'''
for word in wordList:
       focus = NLP.countWordFrequencyInACorpus(processedCorpusFocus, f'{word}')
       file1.write("\r\nHäufigkeit des Vorkommens im Focus: " + focus.__str__())
       taz = NLP.countWordFrequencyInACorpus(processedCorpusTaz, f'{word}')
       file1.write("\r\nHäufigkeit des Vorkommens in der Taz: " + taz.__str__())

'''Create a dictionary with words of all texts from both newspaper'''
#dictionary = NLP.createDictionary(processedCorpusAll)

'''Load the created dictionary with words of all texts from both newspaper'''
dictionary = NLP.loadDictionary()

'''Build word stems from both newpaper and add them to the dictionary'''
#wordStemCorpusAll = NLP.buildWordStemms(processedCorpusAll)
#NLP.addToDictionary(wordStemCorpusAll, dictionary)

'''Build bigrams from both newpaper and add them to the dictionary'''
#bigramsAll = NLP.buildBigramsOfAText(bodysAll)
#NLP.addToDictionary(bigramsAll, dictionary)

NLP.vecotrizeCorpus(dictionary, bodysFocus, 'Focus')  # vectorize bowCorpusFocus
bowCorpusFocus = NLP.loadBowCorpus('Focus')

NLP.vecotrizeCorpus(dictionary, bodysTaz, 'Taz')  # vectorize bowCorpusTaz
bowCorpusTaz = NLP.loadBowCorpus('Taz')

#print('Focus Corpus: ', bowCorpusFocus)
#print('Taz Corpus: ', bowCorpusTaz)

'''Count most common in a Corpus and write them into the WordFrequencies text file (Bag-Of-Words approach)'''
file1.write("\r\n ")
file1.write("\r\nHäufigste Erwähnungen im Focus: " + NLP.createTFIDFModel(bowCorpusFocus, dictionary).__str__())
file1.write("\r\nHäufigste Erwähnungen in der Taz: " + NLP.createTFIDFModel(bowCorpusTaz, dictionary).__str__())


''' Word2Vec approach'''
file2 = open('data/WordSimilarities.txt', 'w')

wordListExt = ['Nachhaltigkeit', 'Armut', 'Hunger', 'Gesunheit', 'Bildung', 'Gleichheit', 'Gleichstellung', 'Trinkwasser', 'Energie', 'Energiewende', 'Menschenwuerde',
                  'Infrastruktur', 'Ungleichheit', 'Stadtenwicklung', 'Konsum', 'Konsumverhalten', 'Klimaschutz', 'Oekosysteme', 'Frieden', 'Partnerschaft',
                  'Wirtschaftswachstum' 'Stadt', 'Meer', 'Lebensraum']

'''Load a extern, pretrained german model word2Vec model'''
''' https://cloud.devmount.de/d2bc5672c523b086/ '''
germanW2vModel = NLP.load_ext_model()

'''Returns a list of the 10 most similar words to a given word from the extern germanwW2vModel'''
for word in wordListExt:
    file2.write(f"\r\nExternes Modell und {word.upper().__str__()} " + NLP.mostSimilar(germanW2vModel, f'{word}').__str__())

'''Create a word2Vec model for the Focus'''
# NLP.save_w2v_model(processedCorpusFocus, 'Focus')

'''Load the Focus word2Vec model'''
w2vModelFocus = NLP.load_w2v_model('Focus')

'''Build word stems from the Focus and add them to the word2Vec model'''
#wordStemCorpusFocus = NLP.buildWordStemms(processedCorpusFocus)
#for wordList in wordStemCorpusFocus:
    #NLP.trainModel(w2vModelFocus, wordList)

'''Build bigrams from the Focus and add them to the word2Vec model'''
#bigramsFocus = NLP.buildBigramsOfAText(bodysFocus)
#for wordList in bigramsFocus:
     #NLP.trainModel(w2vModelFocus, wordList)

'''Returns a list of the 10 most similar words to a given word from the w2VModelFocus and write them into the WordSimilarities text file'''
for word in wordList:
    file2.write(f"\r\nFocus und {word.upper().__str__()} " + NLP.mostSimilar(w2vModelFocus, f'{word}').__str__())

# print('Übereinstimmung von Nachhaltigkeit und Umwelt: ', NLP.checkSimiarity(w2vModelFocus, 'nachhaltigkeit', 'umwelt'))
# print('Höchste Übereinstimmung zu Nachhaltigkeit: ', NLP.checkMostSimilarWord(w2vModelFocus, 'nachhaltigkeit'))

'''Create a word2Vec model for the Taz'''
# NLP.save_w2v_model(processedCorpusTaz, 'Taz')

'''Load the Taz word2Vec model'''
w2vModelTaz = NLP.load_w2v_model('Taz')

'''Build word stems from the Taz and add them to the word2Vec model'''
#wordStemCorpusTaz = NLP.buildWordStemms(processedCorpusTaz)
#for wordList in wordStemCorpusTaz:
    #NLP.trainModel(w2vModelTaz, wordList)

'''Build bigrams from the Focus and add them to the word2Vec model'''
#bigramsTaz = NLP.buildBigramsOfAText(bodysTaz)
#for wordList in bigramsTaz:
     #NLP.trainModel(w2vModelTaz, wordList)

'''Returns a list of the 10 most similar words to a given word from the w2VModelTaz and write them into the WordSimilarities text file'''
for word in wordList:
    file2.write(f"\r\nTaz und {word.upper().__str__()} " + NLP.mostSimilar(w2vModelTaz, f'{word}').__str__())

'''Create a word2Vec model for both newspaper'''
# NLP.save_w2v_model(processedCorpusAll, 'All')

'''Load the All word2Vec model'''
w2vModelAll = NLP.load_w2v_model('All')

'''Build word stems from the Taz and add them to the word2Vec model'''
#wordStemCorpusAll = NLP.buildWordStemms(processedCorpusAll)
#for wordList in wordStemCorpusAll:
    #NLP.trainModel(w2vModelAll, wordList)

'''Build bigrams from the Focus and add them to the word2Vec model'''
#bigramsAll = NLP.buildBigramsOfAText(bodysAll)
#for wordList in bigramsAll:
     #NLP.trainModel(w2vModelAll, wordList)

'''Returns a list of the 10 most similar words to a given word from the w2VModelAll and write them into the WordSimilarities text file'''
for word in wordList:
    file2.write(f"\r\nGesamt und {word.upper().__str__()} " + NLP.mostSimilar(w2vModelAll, f'{word}').__str__())



