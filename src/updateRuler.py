#imports
import spacy
import stanza
from spacy_stanza import StanzaLanguage
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
import pandas as pd
from spacy import displacy

DATA_PATH = '..\\data\\'

# add patterns for given phrases list to ruler with given label(one label per list)
def addPatternsForPhrasesList(ruler, phrasesList, entityLabel):
    for phrase in phrasesList:
        if phrase.strip()!= "":
            doc = nlp.make_doc(phrase.strip())
            token_pattern = [{"lemma": token.lower_} for token in doc]
            ruler.add_patterns([{"label": entityLabel, "pattern": token_pattern}])
            token_pattern = [{"lower": token.lower_} for token in doc]
            ruler.add_patterns([{"label": entityLabel, "pattern": token_pattern}])

#LOAD lexicons
organs = pd.read_csv('{0}{1}'.format(DATA_PATH, "organs.csv"), sep='\n', usecols=['name'], squeeze=True)
complaints = pd.read_csv('{0}{1}'.format(DATA_PATH,"complaints.csv"), sep='\n', usecols=['name'], squeeze=True)
symptoms = pd.read_csv('{0}{1}'.format(DATA_PATH,"symptoms.csv"), sep='\n', usecols=['name'], squeeze=True)
anatomicalSystems = pd.read_csv('{0}{1}'.format(DATA_PATH,"systems.csv"), sep=',', usecols=['name'], squeeze=True)
familyRelations = pd.read_csv('{0}{1}'.format(DATA_PATH,"familyRelations.csv"), sep='\n', usecols=['name'], squeeze=True)
riskFactors = pd.read_csv('{0}{1}'.format(DATA_PATH,"riskFactors.csv"), sep=',', usecols=['name'], squeeze=True)
negations = pd.read_csv('{0}{1}'.format(DATA_PATH,"negations.csv"), sep=',', usecols=['name'], squeeze=True)
familyHistorySynonyms = pd.read_csv('{0}{1}'.format(DATA_PATH,"familyHistorySynonyms.csv"), sep=',', usecols=['name'], squeeze=True)
negationOfComplaints = pd.read_csv('{0}{1}'.format(DATA_PATH,"negationOfComplaints.csv"), sep=',', usecols=['name'], squeeze=True)
negationOfSymptoms = pd.read_csv('{0}{1}'.format(DATA_PATH,"negationOfSymptoms.csv"), sep=',', usecols=['name'], squeeze=True)
negationOfRiskFactors = pd.read_csv('{0}{1}'.format(DATA_PATH,"negationOfRiskFactors.csv"), sep=',', usecols=['name'], squeeze=True)
familyHistory = pd.read_csv('{0}{1}'.format(DATA_PATH,"familyHistory.csv"), sep=',', usecols=['name'], squeeze=True)

#build ruler and save to disk
snlp = stanza.Pipeline(lang="bg")
nlp = StanzaLanguage(snlp)
ruler = EntityRuler(nlp, overwrite_ents=True)

print("Build organs rules...")
addPatternsForPhrasesList(ruler, organs, "ORGAN")
print("Build complaints rules...")
addPatternsForPhrasesList(ruler, complaints, "COMPLAINT")
print("Build symptoms rules...")
addPatternsForPhrasesList(ruler, symptoms, "SYMPTOM")
print("Build anatomicalSystems rules...")
addPatternsForPhrasesList(ruler, anatomicalSystems, "ANATOMICAL_SYSTEM")
print("Build familyRelations rules...")
addPatternsForPhrasesList(ruler, familyRelations, "FAMILY")
print("Build riskFactors rules...")
addPatternsForPhrasesList(ruler, riskFactors, "RISK_FACTOR")
print("Build negations rules...")
addPatternsForPhrasesList(ruler, negations, "NEGATION")
print("Build familyHistorySynonyms rules...")
addPatternsForPhrasesList(ruler, familyHistorySynonyms, "FAMILY_HISTORY_SYNONYM")
print("Build negationOfComplaints rules...")
addPatternsForPhrasesList(ruler, negationOfComplaints, "NO_COMPLAINT")
print("Build negationOfSymptoms rules...")
addPatternsForPhrasesList(ruler, negationOfSymptoms, "NO_SYMPTOM")
print("Build negationOfRiskFactors rules...")
addPatternsForPhrasesList(ruler, negationOfRiskFactors, "NO_RISK_FACTOR")
print("Build familyHistory rules...")
addPatternsForPhrasesList(ruler, familyHistory, "FAMILY_HISTORY")
print("Saving ruler...")
ruler.to_disk("entity_ruler") 
print("Ruler is saved")