from collections import OrderedDict
import whisper
import re
from keybert import KeyBERT
import spacy

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"

valid_symptoms = ["swollen glands", "inflamed glands", "fever", "sore throat", "runny nose", "stuffy nose", "headache", "fatigue", "tiredness", "vomit", "diarrhea"]


def get_all_questions(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]

    question_list = []
    for sentence in sentences:
        if '?' in sentence:
            question_list.append(sentence)
    return question_list

def get_patient_questions(question_list):
    patient_questions_list = []
    for question in question_list:
        if not 'how may I help you' in question:
            if not 'tell me your symptoms' in question:
                if not 'long have you' in question:
                    if not 'treatments have you taken' in question:
                        if not 'any further questions' in question:
                            patient_questions_list.append(question)
    return patient_questions_list

def get_symptoms(transcript):
    symptom_list = []
    for symptom in valid_symptoms:
        if symptom in transcript:
            symptom_list.append(symptom)
    return symptom_list

def get_raw_keywords(transcript):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(transcript)
    words_only = []
    for keys in keywords:
        words_only.append(keys[0])

    return words_only

def get_entities(transcript):
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_lg")
    
    dates = []
    orgs = []
    names = []
    doc = nlp(transcript)
    for entity in doc.ents:
        if 'DATE' in str(entity.label_):
            dates.append(entity.text)
        elif 'ORG' in str(entity.label_):
            orgs.append(entity.text)
        elif 'NAME' in str(entity.label_):
            names.append(entity.text)
    
    nouns = [chunk.text for chunk in doc.noun_chunks]
    nouns = list(OrderedDict.fromkeys(nouns)) 
    verbs =  [token.lemma_ for token in doc if token.pos_ == "VERB"]
    verbs = list(OrderedDict.fromkeys(verbs)) 



    return dates, orgs, names, nouns, verbs

    

model = whisper.load_model("base")
result = model.transcribe("transcript_1.wav")

transcript = result["text"]
patient_questions = get_patient_questions(get_all_questions(transcript))
symptoms = get_symptoms(transcript)
raw_keywords = get_raw_keywords(transcript)
dates, orgs, names, nouns, verbs = get_entities(transcript)

with open('transcript.txt', 'w') as f:
    print(transcript, file=f)
with open('questions).txt', 'w') as f:
    print(patient_questions, file=f)
with open('symptoms.txt', 'w') as f:
    print(symptoms, file=f)
with open('raw_keywords.txt', 'w') as f:
    print(raw_keywords, file=f)
with open('dates.txt', 'w') as f:
    print(dates, file=f)
with open('orgs.txt', 'w') as f:
    print(orgs, file=f)
with open('names.txt', 'w') as f:
    print(names, file=f)
with open('verbs.txt', 'w') as f:
    print(verbs, file=f)


# print(transcript)
print("Patient Questions:")
print(patient_questions)
print("Patient Symptoms")
print(symptoms)
print("Raw Keywords")
print(raw_keywords)
# print("Nouns:")
# # print(nouns)
print("Verbs:")
print(verbs)
