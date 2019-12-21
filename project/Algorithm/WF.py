from mysql.connector import connect
from keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import re

def preProcessing(raw_data):
    stop_words = set(stopwords.words('english'))    #set english stopwords
    ptrn = '[^a-zA-Z]'  # regex for finding non-alphabet characters
    tokens = []
    line_res = []
    n = 0
    for line in raw_data:
        result = []
        word_tokens = word_tokenize(line.lower())   #tokenize & change uppercase characters to lowercase characters
        new_word_tokens = []
        lemmatizer = WordNetLemmatizer()
        for ind, w in enumerate(word_tokens[:]):
            w = lemmatizer.lemmatize(w)                 #lemmatize
            if not re.search(ptrn, word_tokens[ind]):   #find non-alphabet characters
                new_word_tokens.append(word_tokens[ind])
        for w, pos in nltk.pos_tag(new_word_tokens):    #POS-Tagging
            if w not in stop_words and 'cid' not in w and len(w) > 2:   #find stopwords
                    result.append(w)
        tokens.append(result)
        line_res.append(" ".join(tokens[n]))
        n += 1

    corpus = []
    for n in range(len(raw_data)):
        corpus.append(line_res[n])
    return tokens, corpus

def wordCount(corpus):
    new_corpus = [""]
    new_corpus[0] = " ".join(corpus)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(new_corpus)
    word2count = tokenizer.word_counts  #calculate the word counts
    return sorted(word2count.items(), key=lambda x:x[1], reverse=True)[:50]


connection = connect(
    host="52.79.166.26",
    port=3306,
    user="csed232",
    passwd="csed232",
    database="postech",
    auth_plugin="mysql_native_password"
)

cursor = connection.cursor()
query = ("SHOW COLUMNS FROM paper")
cursor.execute(query)
data = cursor.fetchall()

query = ("select degree, title, abstract from paper")   #get degree, title and abstract column's data from DB
cursor.execute(query)
data = cursor.fetchall()

title_list_doc = []
data_doc = []
title_list_mas = []
data_mas = []
for ind, val in enumerate(data):
    if data[ind][0] == 'Doctor':
        title_list_doc.append(data[ind][1])
        data_doc.append(data[ind][2])
    elif data[ind][0] == 'Master':
        title_list_mas.append(data[ind][1])
        data_mas.append(data[ind][2])
connection.commit()

tokens_doc, corpus_doc = preProcessing(data_doc)
tokens_mas, corpus_mas = preProcessing(data_mas)
res_doc = wordCount(corpus_doc)
res_mas = wordCount(corpus_mas)

for i in range(len(res_doc)):
    query = ("insert into WORD_FREQ(id, word, countss, degree) value (%s, %s, %s, %s)")
    val = (i, res_doc[i][0], res_doc[i][1], 'Doctor')
    cursor.execute(query, val)
connection.commit() #send data to DB

for i in range(len(res_mas)):
    query = ("insert into WORD_FREQ(id, word, countss, degree) value (%s, %s, %s, %s)")
    val = (i + len(res_mas), res_mas[i][0], res_mas[i][1], 'Master')
    cursor.execute(query, val)
connection.commit() #send data to DB



