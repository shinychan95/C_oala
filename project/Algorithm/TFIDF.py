from mysql.connector import connect
from preprocessing import preProcessing
from keras.preprocessing.text import Tokenizer


def tfidfKeras(corpus, keyword_num=1):
    t = Tokenizer()
    t.fit_on_texts(corpus)
    mat_tfidf = t.texts_to_matrix(corpus, mode='tfidf')
    arr = mat_tfidf.tolist()    #array to list
    res = []        #list of every keword
    for i in arr:
        res_one = []  # list of keywords from one research paper
        print(i)
        max_ind = sorted(range(len(i)), key=lambda j:i[j], reverse=True)[:keyword_num]
        #find indices of largest elements in array
        for ind in max_ind:
            for a, b in t.word_index.items():
                if b == ind:
                    res_one.append((a, i[b]))
        res.append(res_one)
    return res



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

tokens, corpus = preProcessing(data)
tfidf_res = tfidfKeras(corpus, 5)

for i in range(len(title_list)):
    query = ("insert into TF_IDF(title, key1, key2, key3, key4, key5) value (%s, %s, %s, %s, %s, %s)")
    val = (title_list[i], tfidf_res[i][0], tfidf_res[i][1], tfidf_res[i][2], tfidf_res[i][3], tfidf_res[i][4])
    cursor.execute(query, val)
connection.commit() #send data to DB