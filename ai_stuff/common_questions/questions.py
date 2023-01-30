import re

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"

def split_into_sentences(text):
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
    for sentence in sentence_list:
        if '?' in sentence:
            question_list.append(sentence)
    return question_list

doc = """
Hello, how may I help you today? I'm pretty sure I have the flu and I need advice on how to cope. I'm sorry to hear that. Can you tell me your symptoms? I have a headache, fever, a cough, muscle pain and swollen glands. Okay, it sounds like you have the flu. How long have you been experiencing these symptoms? I've been experiencing these symptoms for three days. What treatments have you taken so far? I've taken some app, some paracetamol and some ibuprofen. Okay, please keep hydrated by drinking plenty of water and electrolytes. Continue on the paracetamol and also continue with the ibuprofen to reduce glandular inflammation. Do you have any further questions? Yes, is this fatal? The flu is not fatal. Can I go into public places? Please do not enter public spaces as this will likely infect others. How long will this last for? The average flu lasts only five days or so. Thanks, that's all the help I need. You're welcome, goodbye.
"""

sentence_list = split_into_sentences(doc)

question_list = []
for sentence in sentence_list:
    if '?' in sentence:
        question_list.append(sentence)

patient_questions_list = []
for question in question_list:
    if not 'how may I help you' in question:
        if not 'tell me your symptoms' in question:
            if not 'long have you' in question:
                if not 'treatments have you taken' in question:
                    if not 'any further questions' in question:
                        patient_questions_list.append(question)

print(patient_questions_list)



