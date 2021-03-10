#imports
import spacy
import stanza
from spacy_stanza import StanzaLanguage
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
import pandas as pd
import re
import os
DATA_PATH = '..\\data\\'

# #LOAD lexicons
lexiconeDic = {
    'ORGAN': list(pd.read_csv('{0}{1}'.format(DATA_PATH, "organs.csv"), sep='\n', usecols=['name'], squeeze=True)),
    'COMPLAINT': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"complaints.csv"), sep='\n', usecols=['name'], squeeze=True)),
    'SYMPTOM': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"symptoms.csv"), sep='\n', usecols=['name'], squeeze=True)),
    'ANATOMICAL_SYSTEM': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"systems.csv"), sep=',', usecols=['name'], squeeze=True)),
    'FAMILY': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"familyRelations.csv"), sep='\n', usecols=['name'], squeeze=True)),
    'RISK_FACTOR': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"riskFactors.csv"), sep=',', usecols=['name'], squeeze=True)),
    'NEGATION': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"negations.csv"), sep=',', usecols=['name'], squeeze=True)),
    'FAMILY_HISTORY_SYNONYM': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"familyHistorySynonyms.csv"), sep=',', usecols=['name'], squeeze=True)),
        
    'NO_COMPLAINT': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"negationOfComplaints.csv"), sep=',', usecols=['name'], squeeze=True)),
    'NO_SYMPTOM': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"negationOfSymptoms.csv"), sep=',', usecols=['name'], squeeze=True)),
    'NO_RISK_FACTOR': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"negationOfRiskFactors.csv"), sep=',', usecols=['name'], squeeze=True)),
    'FAMILY_HISTORY': list(pd.read_csv('{0}{1}'.format(DATA_PATH,"familyHistory.csv"), sep=',', usecols=['name'], squeeze=True)),
}


def saveNewAnotationsInHistory():
    savedAnotations = pd.read_csv('{0}{1}'.format(DATA_PATH,"saved_anotations.csv"), sep=',', squeeze=True)
    df = pd.DataFrame(tuple(row) for row in savedAnotations.values)
    column_names = ["sentense", "entities"]
    historyAnotations = '{0}{1}'.format(DATA_PATH,"saved_anotations_history.csv")
    # if file does not exist write header 
    if not os.path.isfile(historyAnotations):
       df.to_csv(historyAnotations, header=column_names, index=False)
    else: # else it exists so append without writing the header
       df.to_csv(historyAnotations, mode='a', header=False, index=False)

def loadNewAnotations():
    savedAnotationsPath = '{0}{1}'.format(DATA_PATH,"saved_anotations.csv")
    savedEntitiesLists = pd.read_csv(savedAnotationsPath, sep=',', usecols=['entities'], squeeze=True)
    result = {}
    import ast
    for row in savedEntitiesLists.values:
        listOfTuples = ast.literal_eval(row)
        for object in listOfTuples:
            result[object[0]] = object[3]
    if os.path.exists(savedAnotationsPath):
        os.remove(savedAnotationsPath)
    return result

def getLexiconePathByClass(className):
    return {
        'ORGAN': '{0}{1}'.format(DATA_PATH, "organs.csv"),
        'COMPLAINT': '{0}{1}'.format(DATA_PATH,"complaints.csv"),
        'SYMPTOM': '{0}{1}'.format(DATA_PATH,"symptoms.csv"),
        'ANATOMICAL_SYSTEM': '{0}{1}'.format(DATA_PATH,"systems.csv"),
        'FAMILY': '{0}{1}'.format(DATA_PATH,"familyRelations.csv"),
        'RISK_FACTOR': '{0}{1}'.format(DATA_PATH,"riskFactors.csv"),
        'NEGATION': '{0}{1}'.format(DATA_PATH,"negations.csv"),
        'FAMILY_HISTORY_SYNONYM': '{0}{1}'.format(DATA_PATH,"familyHistorySynonyms.csv"),
        
        'NO_COMPLAINT': '{0}{1}'.format(DATA_PATH,"negationOfComplaints.csv"),
        'NO_SYMPTOM': '{0}{1}'.format(DATA_PATH,"negationOfSymptoms.csv"),
        'NO_RISK_FACTOR': '{0}{1}'.format(DATA_PATH,"negationOfRiskFactors.csv"),
        'FAMILY_HISTORY': '{0}{1}'.format(DATA_PATH,"familyHistory.csv"),
    }[className]

def saveObjectToLexicone(object, lexiconeName):
    lexiconeDF = pd.DataFrame([object], columns=['name'])
    lexiconeDF.to_csv(lexiconeName, mode='a', header=False, index=False)
    
def removeObjectFromLexicone(object, lexicone):
    lexiconePath = getLexiconePathByClass(lexicone)
    print(lexiconePath)
    df = pd.read_csv(lexiconePath, sep='\n')
    df = df.drop(df.query('name=="{0}"'.format(object)).index)
    df.shape
    df.to_csv(lexiconePath, header=["name"], index=False)
    
def updateItemInLexicones(object, objectType):
    print(object, objectType)
    for key, value in lexiconeDic.items():
        if object in value and objectType != key:
            print("remove")
            removeObjectFromLexicone(object, key)
        if object not in value and objectType==key:
            print("add")
            saveObjectToLexicone(object, getLexiconePathByClass(key))
    
print("Добавяне на записаните анотации към лексиконите...") 
if os.path.isfile('{0}{1}'.format(DATA_PATH,"saved_anotations.csv")):
    saveNewAnotationsInHistory()
    for key, value in loadNewAnotations().items():
        updateItemInLexicones(key, value)
print("Записаните анотации бяха добавени към лексиконите.")   