
import kleis.resources.dataset as kl
import nltk
import mysql.connector


def main():
    #bring data from database

    connection = mysql.connector.connect(
        host="52.79.166.26",
        port=3306,
        user="csed232",
        passwd="csed232",
        database="postech",
        auth_plugin="mysql_native_password"
    )

    cursor = connection.cursor()

    query = ("select title, abstract from paper")

    cursor.execute(query)

    data = cursor.fetchall()

    str_r=[]

    for i in data:
        """Method to run package."""

     #     # Load default dataset

        default_corpus = kl.load_corpus()


        text = i[1]
        print(text)
          # Train or load model

        default_corpus.training(filter_min_count=3)

        keyphrases = default_corpus.label_text(text)

        keyword = ""

        for keyphrase in keyphrases:
             keyphrase_id, (keyphrase_label_, (start, end)), keyphrase_str = keyphrase
             str_r.append(keyphrase_str)

        str_r = list(set(str_r))

        #insert keywords to database
            #query = ("insert into crf(title, keyword) values(%s, %s)")

            #cursor.execute(query, (i[0], str(str_r)))
        print(str_r)
        print("\n")
        str_r=[]

    connection.commit()

if __name__ == "__main__":
    main()
