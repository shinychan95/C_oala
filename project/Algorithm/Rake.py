import RAKE
import mysql.connector

connection = mysql.connector.connect(
    host="52.79.166.26",
    port=3306,
    user="csed232",
    passwd="csed232",
    database="postech",
    auth_plugin="mysql_native_password"
)

cursor = connection.cursor()

def create_table():
    query = ("create table postech.RAKE(id VARCHAR(10),title VARCHAR(100),1st_keyword VARCHAR(100),2nd_keyword VARCHAR(100),3rd_keyword VARCHAR(100))")
    cursor.execute(query)

def delete_table():
    query=("DROP table RAKE")
    cursor.execute(query)

def get_data_from_db():
    query = ("select title, abstract from paper")
    cursor.execute(query)
    data = cursor.fetchall()

    titles=[i[0]for i in data]
    for i in range(47):
        titles[i]=titles[i][:-1]
    data = [i[1] for i in data]

    return (titles,data)



(titles,text_set)=get_data_from_db()

Rake = RAKE.Rake(RAKE.SmartStopList())

keyword_list = []
for i in range(len(text_set)):
    keyword_list.append(Rake.run(text_set[i],maxWords=4))

sql = """INSERT INTO postech.RAKE (id,title,1st_keyword,2nd_keyword,3rd_keyword) VALUES (%s, %s, %s, %s, %s)"""
val = []

for i in range(len(text_set)):  # 논문 개수
    temp_keywod_list=[]
    for j in range(3):  # 추출 단어 개수
        print(keyword_list[i][j])
        temp_keywod_list.append(keyword_list[i][j][0])
    val.append((str(i+1),titles[i],temp_keywod_list[0],temp_keywod_list[1],temp_keywod_list[2]))
    print('\n\n')

delete_table()
create_table()

query=("ALTER TABLE postech.RAKE MODIFY COLUMN title VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;")
cursor.execute(query)
query=("ALTER TABLE postech.RAKE MODIFY COLUMN 1st_keyword VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;")
cursor.execute(query)
query=("ALTER TABLE postech.RAKE MODIFY COLUMN 2nd_keyword VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;")
cursor.execute(query)
query=("ALTER TABLE postech.RAKE MODIFY COLUMN 3rd_keyword VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;")
cursor.execute(query)

cursor.executemany(sql,val)
connection.commit()
print(cursor.rowcount, "record was inserted")

