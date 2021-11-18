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