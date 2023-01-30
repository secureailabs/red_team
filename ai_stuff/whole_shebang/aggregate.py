from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import spacy

def read_csv(file_name):
    txt_file = open(file_name, "r")
    file_content = txt_file.read()
    content_list = file_content.split(";")
    txt_file.close()
    rep = []
    for element in content_list:
        rep.append(element.replace("\n", ""))
    content_list = rep
    return content_list

def aggregate_files(file_name):
    list = read_csv("patient_1/"+file_name+".txt") + read_csv("patient_2/"+file_name+".txt")
    with open("aggregate/"+file_name+".txt", 'w') as f:
        print(*list, sep=";", file=f)


def wordwall(file_name):
    comment_words = ''
    content = read_csv("agg_"+file_name+".txt")

    for val in content:

        # typecaste each val to string
        val = str(val)
    
        # split the value
        tokens = val.split()
        
        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = set(STOPWORDS),
                min_font_size = 10).generate(comment_words)
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    plt.savefig("images/"+file_name+".png")

def faq():
    scores = []
    questions = read_csv("aggregate/questions.txt")
    nlp = spacy.load("en_core_web_lg")
    for question_1 in questions:
        q1 = nlp(question_1)
        score = 0
        for question_2 in questions:
            q2 = nlp(question_2)
            score += q1.similarity(q2)
        scores.append(score)

    faqs = []
    for score, question in zip(scores, questions):
        faqs.append([score, question])

    faqs = sorted(faqs, key=lambda x: x[0], reverse=True)

    with open('aggregate/faqs.txt', 'w') as f:
        print(faqs, sep='; ', file=f)
    return

file_names = ["questions", "raw_keywords", "symptoms", "verbs", "names", "orgs", "dates"]
word_wall_names = ["raw_keywords", "symptoms", "verbs", "names", "orgs"]


for name in file_names:
    aggregate_files(name)

for name in word_wall_names:
    wordwall(name)

faq()

