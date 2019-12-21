from mysql.connector import connect
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models import CoherenceModel
import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.gensim as gensimvis
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

def LDA(tokens, start, stop, step=1):
    dictionary = Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]
    model_list = []
    coherence_values = []
    max_topic_num = 0
    for i in range(start, stop, step):
        print('steps  ', i)
        model = LdaModel(corpus, id2word=dictionary, num_topics=i + 1)  #LDA model
        model_list.append(model)
        coherence_model_lda = CoherenceModel(model, texts=tokens, dictionary=dictionary, coherence='c_v')   #Coherence
        coherence_lda = coherence_model_lda.get_coherence()             #calculate the coherence score
        if i is not start and coherence_lda > max(coherence_values):
            max_topic_num = i
        coherence_values.append(coherence_lda)

    x = range(start, stop, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()  #show graph of coherence score by pyplot
    max_ind = coherence_values.index(max(coherence_values))
    model_list[max_ind].save("result_model")
    prepared_data = gensimvis.prepare(model_list[max_ind], corpus=corpus, dictionary=dictionary)
    pyLDAvis.save_html(prepared_data, 'res.html')   #save the result of LDA by html file
    pyLDAvis.save_json(prepared_data, 'res.json')   #save the result of LDA by JSON file
    return model_list[max_ind], coherence_values[max_ind], max_topic_num


def main():
    connection = connect(
        host="52.79.166.26",
        port=3306,
        user="csed232",
        passwd="csed232",
        database="postech",
        auth_plugin="mysql_native_password"
    )

    cursor = connection.cursor()    #connect to DB
    query = ("SHOW COLUMNS FROM paper")
    cursor.execute(query)
    data = cursor.fetchall()

    query = ("select title, abstract from paper")   #get title, abstract column's data
    cursor.execute(query)
    data = cursor.fetchall()
    title_list = [i[0] for i in data]
    data = [i[1] for i in data]
    connection.commit()

    tokens, corpus = preProcessing(data)  #preprocessing
    model_max, coherence_max, topic_num_max = LDA(tokens, 17, 18, step = 1)
    model_max.save("res_model") #save the LDA model
    #hyper-parameter for topic number : 18
    #check the image which presents the result of experiment for finding the best topic number
    print(topic_num_max)


if __name__ == '__main__':
    main()




