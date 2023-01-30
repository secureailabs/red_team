import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_lg")

# Process whole documents
doc = """
Hello, how may I help you today? I'm pretty sure my son John may have the flu and I need advice on how to cope. I'm sorry to hear that. Can you tell me your symptoms? I have a headache, fever, a cough, muscle pain and swollen glands. Okay, it sounds like you have the flu. How long have you been experiencing these symptoms? I've been experiencing these symptoms for three days. What treatments have you taken so far? I've taken some app, some paracetamol and some ibuprofen. Okay, please keep hydrated by drinking plenty of water and electrolytes. Continue on the paracetamol and also continue with the ibuprofen to reduce glandular inflammation. Do you have any further questions? Yes, is this fatal? The flu is not fatal. Can I go into public places? Please do not enter public spaces as this will likely infect others. How long will this last for? The average flu lasts only five days or so. Thanks, that's all the help I need. You're welcome, goodbye.
"""
doc = nlp(doc)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)


doc1 = nlp("Will I die.")
doc2 = nlp("That looks delicious.")
doc3 = nlp("Is it going to kill me")

# Similarity of two documents
print(doc1, "<->", doc2, doc1.similarity(doc2))
print(doc1, "<->", doc3, doc1.similarity(doc3))
print(doc3, "<->", doc2, doc3.similarity(doc2))

