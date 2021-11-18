import pandas as pd

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
Cleans data for authors
IN: collection = collection of json files from mongodb
OUT: dfTazClean = dataframe of a collection (json files from mongodb) with adjusted authors 
'''
def cleanTazMetaData(collectionTaz):
    dfTaz = transformDataToDf(collectionTaz)
    dfTazClean = dfTaz.replace({'Hommage an Rockband Ton Steine Scherben': 'Author nicht bekannt',  #clean up all missing or corrupted Data
                            'Ex-Ministerin Wara Wende im Interview': 'Author nicht bekannt',
                            'Jagoda Marinić über realen Wandel': 'Author nicht bekannt',
                            'Pandemiegeschehen 2021': 'Author nicht bekannt',
                            'Freie Stellen bei der taz': 'Author nicht bekannt',
                            'Warum Fehler gut sind': 'Author nicht bekannt',
                            'kritisch betrachtet: Corona-Impfstoff': 'Author nicht bekannt',
                            'Indien liberalisiert den Agrarsektor': 'Author nicht bekannt',
                            'Coronahilfen für Selbständige': 'Author nicht bekannt',
                            'Neuer Erfolg von taz zahl ich': 'Author nicht bekannt',
                            'Freikarten für Online-Theater gewinnen': 'Author nicht bekannt',
                            'Christina Schlag und Schlecky Silberstein': 'Author nicht bekannt',
                            'Wahrheitbei Tomüber die Wahrheit': 'Tom über die Wahrheit'})

    return dfTazClean