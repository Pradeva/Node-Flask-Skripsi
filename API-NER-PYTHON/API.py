from flask import Flask, request
from flask_mysqldb import MySQL
from pathlib import Path
import spacy
import json

app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kuliah'

mysql = MySQL(app)

# MASTER NATURAL LANGUAGE

# CREATE NATURAL LANGUAGE

@app.route('/master/NL/add', methods=['GET', 'POST'])
def NaturalLanguage():
    try:
        id_data = request.json['id_data']

        con = request.json['condition']
        act = request.json['action']

        # Simpan hasil ke dalam tabel MySQL
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO natural_language (data_id, `condition`, action) values (%s, %s, %s)",
                       (id_data, con, act))
        mysql.connection.commit()
        cursor.close()

        response = {
            "status": "success",
            "message": "Data successfully inserted into the database."
        }
        return json.dumps(response)
    
    except Exception as e:
        return str(e), 500

@app.route('/get/ner', methods=['GET', 'POST'])
def NlpToNer():
    try:
        nl_id = request.json['nl_id']
        con = request.json['condition']

        output_dir = Path(r"C:\Users\prade\OneDrive\Documents\Materi Kuliah\Sitasi Proposal\FINAL PROPOSAL\Node-Flask-Api\MODEL")

        nlp = spacy.load(output_dir)

        panjang = len(con)

        print(panjang)

        doc = nlp(con)

        res = []

        for ent in doc.ents:

            temp = []

            # cursor = mysql.connection.cursor()
            # cursor.execute("INSERT INTO ner (nl_id, sentence, label, start, end) values (%s, %s, %s, %s, %s)",
            #             (nl_id, ent.text, ent.label_, ent.start_char, ent.end_char))
            # mysql.connection.commit()
            # cursor.close()

            temp.append(ent.text)
            temp.append(ent.label_)
            temp.append(ent.start_char)
            temp.append(ent.end_char)
            res.append(temp)
        
        for i in range(len(res)):
            print(res[i])


        Result = {
            "status": "success",
            "message": "Data successfully generated."
        }
        json_string = json.dumps(Result)
        return json_string

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
