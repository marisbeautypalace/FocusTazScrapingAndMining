import unittest
from Taz import MetaDataAnalysis as mda
from Common import HypothesenAnalysis as he
from Common import DatabaseConnection as dbc
from Common import DataCleaning as dc

class AnalysisTest(unittest.TestCase):

    def test_getNumberOfUniqueAuthors(self):
        dfTest = dc.transformDataToDf(dbc.collectionTest)
        numberOfUniqueAuthors = mda.getNumberOfUniqueAuthors(dfTest)
        self.assertEqual(numberOfUniqueAuthors, 5)

    def test_getNumberOfWordsForBodysForEveryArticle(self):
        dfTest = dc.transformDataToDf(dbc.collectionTest)
        numberOfWords = he.getNumberOfWordsForBodysForEveryArticle(dfTest)
        self.assertEqual(sum(numberOfWords), 5685)

    def test_getNumberOfHitsForWordsInBody(self):
        dfTest = dc.transformDataToDf(dbc.collectionTest)
        sustainabilityWords = ['Nachhaltigkeit',
                               'Klimawandel',
                               'Umweltschutz']

        count = he.getNumberOfHitsForWordsInBody(dfTest, sustainabilityWords)
        self.assertEqual(count, 6)

if __name__ == '__main__':
    unittest.main()