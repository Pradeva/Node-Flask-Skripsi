from flask import Flask
from pathlib import Path
import spacy
import json

app = Flask(__name__)

@app.route('/get/ner/<number>', methods=['GET', 'POST'])
def welcome(number):
    output_dir=Path("/home/pradeva/Documents/NER-API/MODEL")

    nlp = spacy.load(output_dir)

    doc = nlp(number)

    res={}

    i = 1
    for ent in doc.ents:
        temp = {}
        temp[ent.label_] = ent.text
        res[i] = temp
        i = i + 1

    json_string = json.dumps(res)
    return json_string

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)