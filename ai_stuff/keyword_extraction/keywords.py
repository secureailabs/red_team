# script.py
from keybert import KeyBERT

doc = """
Hello, how may I help you today? I'm pretty sure I have the flu and I need advice on how to cope. I'm sorry to hear that. Can you tell me your symptoms? I have a headache, fever, a cough, muscle pain and swollen glands. Okay, it sounds like you have the flu. How long have you been experiencing these symptoms? I've been experiencing these symptoms for three days. What treatments have you taken so far? I've taken some app, some paracetamol and some ibuprofen. Okay, please keep hydrated by drinking plenty of water and electrolytes. Continue on the paracetamol and also continue with the ibuprofen to reduce glandular inflammation. Do you have any further questions? Yes, is this fatal? The flu is not fatal. Can I go into public places? Please do not enter public spaces as this will likely infect others. How long will this last for? The average flu lasts only five days or so. Thanks, that's all the help I need. You're welcome, goodbye.
"""

kw_model = KeyBERT()
print(kw_model.extract_keywords(doc))

print(kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words=None))