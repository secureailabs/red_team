def read_csv(file_name):
    txt_file = open(file_name, "r")
    file_content = txt_file.read()
    content_list = file_content.split(";")
    txt_file.close()
    return content_list

questions = read_csv("patient_1/questions.txt") + read_csv("patient_2/questions.txt")

rep = []
for question in questions:
    rep.append(question.replace("\n", ""))
questions = rep
print(questions)