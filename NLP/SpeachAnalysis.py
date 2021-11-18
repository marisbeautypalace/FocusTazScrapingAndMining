import codecs
from collections import defaultdict
import numpy as np
from gensim.models.phrases import Phraser, Phrases
from nltk.corpus import stopwords
import gensim
from gensim import corpora
from gensim import models
from gensim.models import Word2Vec, KeyedVectors
from gensim.similarities import MatrixSimilarity
from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from HanTa import HanoverTagger as ht

class NLPObject:

    '''
    Check in a Corpus of documents, the similarity of a text/document to the other texts/documents
    IN: rawCorpus = Corpus of documents/texts
    OUT: euclidean_distances = distance of the first dokument in a corpus to the other documents
    '''
    def checkSimilaritiesOfDocs(self, rawCorpus):

        vec = CountVectorizer()

        features = vec.fit_transform(rawCorpus).todense()

        for index in features:
            return (euclidean_distances(features[0], index))

    '''
    Append current text from a file to a raw-corpus
    IN: fileName = name of the file which should be append, rawCorpus = Corpus of documents/texts
    '''
    def appendTextToCorpus(self, fileName, rawCorpus):

        file = codecs.open(fileName, "r", "utf-8")
        text = file.read()
        file.close()
        rawCorpus.append(text)

    '''
    Split rawCorpus in documents/texts and then split docouments/texts in words
    Remove stopwords with german stopwordList
    IN: rawCorpus = Corpus of documents/texts
    OUT: processedCorpus = tokenized Corpus without stopwords
    '''
    def processCorpus(self, rawCorpus):

        stopList = set(stopwords.words('german'))

        processedCorpus = [[word for word in document.lower().split() if word not in stopList] for document in rawCorpus]

        return processedCorpus


    '''
    Lemmatize sentence in german
    IN: processedCorpus = tokenized Corpus without stopwords
    OUT: list = list of stemmwords 
    '''
    def lemmatizeText(self, processedCorpus):

        tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        tags = tagger.tag_sent(processedCorpus)
        list = []

        for stemm in tags:
            list.append(stemm[1])

        return list

    '''
    Build word stemms of  a processedCorpus
    IN: processedCorpus = tokenized Corpus without stopwords
    OUT: list = list of documents/texts with associated stemwords
    '''
    def buildWordStemms(self, processedCorpus):

        i = 0
        list = []
        for text in processedCorpus:
            list.append(self.lemmatizeText(processedCorpus[i]))
            i += 1

        return list

    '''
    Build bigram tokens of a text and make a list of them
    IN: rawCorpus = rawCorpus = Corpus of documents/texts
    OUT: bigramTokens = list of bigram tokens
    '''
    def buildBigramsOfAText(self, rawCorpus):

        tokens = [text.lower().split(" ") for text in rawCorpus]
        bigram = Phrases(tokens, min_count=1, threshold=1, delimiter=b' ')
        bigramPhraser = Phraser(bigram)

        bigramTokens = []
        for sent in tokens:
            bigramTokens.append(bigramPhraser[sent])

        for text in bigramTokens:
            for word in text:
                word.lower()

        return bigramTokens

    '''
    Count frequencies of words in a corpus
    IN: procesedCorpus = tokenized Corpus without stopwords, name = name of a word which frequency should be count
    OUT: frequeny = name of the word plus its  frequency
    '''
    def countWordFrequencyInACorpus(self, processedCorpus, name):

     frequency = defaultdict(int)

     for text in processedCorpus:
         for token in text:
             if(token == f'{name}'):
              frequency[token] += 1

     return frequency

    '''
    Count of words, which are more than i times in a corpus
    IN: procesedCorpus = tokenized Corpus without stopwords, i = number of counts 
    OUT: words = words which are i times or more in a text
    '''
    def countFrequentlyWords(self, processedCorpus, i):

         words = ''
         frequency = defaultdict(int)

         for text in processedCorpus:
             for word in text:
                 frequency[word] += 1

                 if (frequency[word] >= i):
                     words += word + ", "

         return (words)

# Bag-of-Words approach:

    '''
    Create a dictionary and save it
    IN: processedCorpus = tokenized Corpus without stopwords or with stemwords or bigram tokens
    OUT: dictionary = dictionary with Id of a word an its frequency in a Corpus
    '''
    def createDictionary(self, processedCorpus):

        dictionary = corpora.Dictionary(processedCorpus)

        dictionary.save('Dictionaries/newspaper.dict')

        return dictionary

    '''
    Add new Corpus to an existing dictionary
    IN: processedCorpus = tokenized Corpus without stopwords or with stemwords or bigram tokens, 
        dictionary = created dictionary which is saved in the Dictionaries folder
    OUT: dictionary = dictionary with new words(Ids) and their frequencies
    '''
    def addToDictionary(self, processedCorpus, dictionary):

        # update dictionary
        dictionary.add_documents(processedCorpus)

        dictionary.save('Dictionaries/newspaper.dict')

        return dictionary

    '''
    Loads a saved Dictionary
    OUT: loadedDict = current dictionary 
    '''
    def loadDictionary(self):

      #load them back
      loadedDict = corpora.Dictionary.load('Dictionaries/newspaper.dict')

      return loadedDict

    '''
    Vectorize a corpus into a bag-of-words model and save it
    Change every single word into a vector with id and word frequency 
    IN: dictionary = current dictionary, corpus = corpus of documents/texts, 
        name = name of the corpus which will be saved as bag-of-words 
    OUT: bowCorpus = bag-of-words of the input corpus
    '''
    def vecotrizeCorpus(self, dictionary, corpus, name):

        bowCorpus = [dictionary.doc2bow(simple_preprocess(text)) for text in corpus]

        # save corpus
        corpora.MmCorpus.serialize(f'Corpara/{name}.mm', bowCorpus)

        return bowCorpus

    '''
    Loads a saved bowcorpus model
    IN:  name = name of the corpus which will be load as bag-of-words 
    OUT: bowCorpus = bag-of-words of the loaded corpus 
    '''
    def loadBowCorpus(self,name):

        bowCorpus = corpora.MmCorpus(f'Corpara/{name}.mm')

        return bowCorpus

    '''
    Show the word frequencies in bowCorpus model
    IN: bowCorpus = bag-of-words of a loaded corpus model, dictionary = current dictionary
    OUT: words an its frequencies in a bag-of-word
    '''
    def showWordWeightsInCorpus(self, bowCorpus, dictionary):

            for document in bowCorpus:
                print([[dictionary[id], freq] for id, freq in document])

    '''
    Create the TF-IDF model with most common words in a bag-of-words model
    IN: bowCorpus = bag-of-words of a loaded corpus model, dictionary = current dictionary
    OUT: most common words in a corpus of documents/texts
    '''
    def createTFIDFModel(self, bowCorpus, dictionary):

        tfidf = models.TfidfModel(bowCorpus, smartirs='ntc')

        for document in tfidf[bowCorpus]:
            return ([[dictionary[id], np.around(freq, decimals=2)] for id, freq in document])

    '''
    Equal a text with a current bag-of-words-corpus
    IN: bowCorpus = bag-of-words of a loaded corpus model, dictionary = current dictionary,
        text =  a document/text to be compare with a bag-of-words
    OUT: relativeFrequency = relative frequencies of words in a document/text
    '''
    def equalTextWithAModel(self, bowCorpus, dictionary, text):

     tfidf = models.TfidfModel(bowCorpus)

     relativeFrequency = tfidf[dictionary.doc2bow(text.lower().split())]

     return relativeFrequency

    '''
    Equal the similarity of two different corpora
    IN: bowCorpusOne = bag-of-words of a loaded corpus model, bowCorpusTwo = bag-of-words of a loaded corpus model
    OUT: similar = matrix which similarities of all texts in both corpora
    '''
    def equalDifferentCorpara(self, bowCorpusOne, bowCorpusTwo):

        index = MatrixSimilarity(bowCorpusOne)

        similar = index[bowCorpusTwo]

        return similar

# Word2Vec approach:

    '''
    Create a new word2Vec model and save it
    IN: processedCorpus = processedCorpus = tokenized Corpus without stopwords or with stemwords or bigram tokens,
        name = given name of a word2Vec model
    '''
    def save_w2v_model(self, processedCorpus, name):

         # train model
         model = Word2Vec(processedCorpus, min_count=1)  # min_count how often is an word minimum in a text

         # save model
         model.save(f'W2VModels/{name}.bin')

    '''
    Load a pre trained word2Vec model
    IN: name = name of a word2Vec model
    OUT: model = existing word2Vec model
    '''
    def load_w2v_model(self, name):

         # load model
         model = Word2Vec.load(f'W2VModels/{name}.bin')

         return model

    '''
    Load the extern, pre trained word2Vec model
    OUT: model = existing, extern word2Vec model
    '''
    def load_ext_model(self):

        model = gensim.models.KeyedVectors.load_word2vec_format('ExtModels/german.model', binary=True)

        return model

    '''
    Add a text to an existing model to train them and save the new model
    IN: model = existing word2Vec model, text = a new processed text
    OUT: model = new trained model
    '''
    def trainModel(self, model, wordList):

        model.train([[wordList]], total_examples=1, epochs=1)

        # save model
        model.save(f'W2VModels/{model}.bin')

        return model

    '''
    Matches the ten most similar words of a model
    IN: model = existing word2Vec model, word = word to be checked for similarity 
    OUT: ten most similar words which exist in a trained model
    '''
    def mostSimilar(self, model, word):

        try:
            return model.wv.most_similar(f'{word}')
        except KeyError:
            return "word is not in the model!"

    '''
    Compare the similarity of 2 words from a model
    IN: model = existing word2Vec model, word1/word2 = words to be checked for similarity 
    OUT: similarity of the two words of a model in percent
    '''
    def checkSimiarity(self, model, word1, word2):

        try:
            return model.wv.similarity(f'{word1}', f'{word2}')
        except KeyError:
            return "one of the words are not in the model!"

    '''
    Check a word and search the most similar word to it in a model
    IN: model = existing word2Vec model, word = word to be checked for similarity 
    OUT: most similar word of a model to the given word
    '''
    def checkMostSimilarWord(self, model, word):

        try:
            result = model.wv.similar_by_word(f"{word}")
            most_similar_key, similar = result[0]  # look at the first match

            return (f"{most_similar_key}: {similar:.4f}")
        except KeyError:
            return "word is not in the model!"






































