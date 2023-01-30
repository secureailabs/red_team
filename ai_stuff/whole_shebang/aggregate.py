def read_csv(file_name):
    txt_file = open(file_name, "r")
    file_content = txt_file.read()
    content_list = file_content.split(";")
    txt_file.close()
    return content_list

def aggregate_files(file_name):
    list = read_csv("patient_1/"+file_name+".txt") + read_csv("patient_2/"+file_name+".txt")
    rep = []
    for element in list:
        rep.append(element.replace("\n", ""))
    list = rep
    with open("agg_"+file_name+".txt", 'w') as f:
        print(*list, sep=";", file=f)

aggregate_files("questions")
aggregate_files("raw_keywords")
aggregate_files("symptoms")
aggregate_files("verbs")
aggregate_files("names")
aggregate_files("orgs")
aggregate_files("dates")