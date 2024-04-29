from flask import Flask, request, send_file
from flask_mysqldb import MySQL
from pathlib import Path
import spacy
import json
import itertools
from fpdf import FPDF
import random
import string
# from telegram.ext import Updater, CommandHandler
from telegram import Bot
import os
import requests
import time


def check_index(array, value):
    try:
        return array.index(value)
    except ValueError:
        return -1
    
def result_of_logic(array):
    temp1 = []
    temp2 = []
    print("result of logic arra : ", array)
    while (len(array) > 1):
        print("++!!++!!")
        ind_and = check_index(array,"dan")
        print("ind_and", ind_and)
        if (ind_and != -1):

            print("ind_and-1 : ",ind_and-1)
            
            for i in range(ind_and-1):
                temp1.append(array[i])
            
            for i in range(ind_and+2, len(array)):
                temp2.append(array[i])

            print("temp1, temp2, ", temp1, temp2)
                
            result = "True" if array[ind_and-1] == "True" and array[ind_and+1] == "True" else "False"
            temp1.append(result)
            
            array = temp1 + temp2
            temp1, temp2 = [], []
        else:
             result = "True" if array[0] == "True" or array[2] == "True" else "False"
             array.pop(0)
             array.pop(0)
             array[0] = result


app = Flask(__name__)


# nl_id = request.json['nl_id']
# con = "Jenis komputer sama dengan Server dan Jumlah RAM lebih dari 128"
# act = "spek sesuai"
@app.route('/get/ner', methods=['GET', 'POST'])
def NlpToNer():
    try:
        # con = "Jenis kable sama dengan CAT6 dan Area sama dengan Regional Reog"
        # act = "Data Stored"
        con = request.json['condition']
        act = request.json['action']
        # buat juga input action

        output_dir = Path(r"C:\Users\prade\OneDrive\Documents\Materi Kuliah\Sitasi Proposal\FINAL PROPOSAL\Api\Node-Flask-Api\MODEL")

        nlp = spacy.load(output_dir)

        panjang = len(con)
        total_aksi = 0
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        array_gate = []
        doc = nlp(con)

        print(panjang)

        res = []

        for ent in doc.ents:

            temp = []

            temp.append(ent.text)
            temp.append(ent.label_)
            if ent.label_ == "Relas":
                total_aksi += 1
            elif ent.label_ == "Gate":
                array_gate.append(ent.text)
            temp.append(ent.start_char)
            temp.append(ent.end_char)
            res.append(temp)

        # Hasil array untuk menyimpan semua kombinasi
        hasil_array = []

        # Hasilkan semua kombinasi
        for kombinasi in itertools.product(["False", "True"], repeat=total_aksi):
            hasil_array.append(list(kombinasi))

        # Transpose array
        hasil_array_transpose = list(map(list, zip(*hasil_array)))

        # Cetak hasil
        # for kombinasi in hasil_array_transpose:
        #     print(kombinasi)

        header_condition = []

        header_condition.append("C/N")

        for i in range(2**total_aksi):
            header_condition.append(i+1)

        array_kalimat_kondisi = []
        # array_kalimat_kondisi.append(header_condition)
        for i in range(len(res)):
            print(res[i])
            
            if res[i][1] == "Relas":
                kalimat = ""
                # buat asumsi jika indeks 0 adalah gate, maka akan tidak valid
                if (i == 0):
                    kalimat = kalimat + con[0:res[i][2]]
                    kalimat = kalimat + res[i][0]
                    kalimat = kalimat + con[res[i][3]:res[i+1][2]]
                    array_kalimat_kondisi.append([kalimat])
                elif(i == len(res)-1):
                    kalimat = kalimat + con[res[i-1][3]:res[i][2]]
                    kalimat = kalimat + res[i][0]
                    kalimat = kalimat + con[res[i][3]:panjang]
                    array_kalimat_kondisi.append([kalimat])
                else:
                    kalimat = kalimat + con[res[i-1][3]:res[i][2]]
                    kalimat = kalimat + res[i][0]
                    kalimat = kalimat + con[res[i][3]:res[i+1][2]]
                    array_kalimat_kondisi.append([kalimat])
        print(array_kalimat_kondisi)

        array_kondisi = []
        if(len(hasil_array_transpose) == len(array_kalimat_kondisi)):
            for i in range(len(hasil_array_transpose)):
                array_kondisi.append([alphabet[i % len(alphabet)]]+hasil_array_transpose[i])
        nilai_kondisi = array_kondisi
        array_kondisi = [header_condition] + array_kondisi
        # print(array_kondisi, nilai_kondisi, array_gate)

        print(array_kondisi)

        print("__________________________")
        arr_result = []
        arr_result.append('R')
        for arr in hasil_array:
            result = []
            max_length = max(len(arr), len(array_gate))

            for i in range(max_length):
                if i < len(arr):
                    result.append(arr[i])
                if i < len(array_gate):
                    result.append(array_gate[i])
            # print(result, result_of_logic(result))
            arr_result.append(result_of_logic(result))
        print("__________________________")

        # PEMBUATAN PDF =========================================================================================
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", size=12)

        teks_atas = 'Test Case'

        # Tambahkan teks di atas tabel pertama
        pdf.set_xy(10, 10)
        pdf.cell(0, 5, teks_atas, ln=True, align='C')

        pdf.ln(10)

        con_text = "Kondisi : " + con
        act_text = "Aksi    : " + act

        pdf.cell(0, 5, con_text, ln=True, align='L')
        pdf.cell(0, 5, act_text, ln=True, align='L')

        pdf.ln(5)

        for i in range(len(array_kalimat_kondisi)):
            teks_kondisi = alphabet[i % len(alphabet)] + " : " + array_kalimat_kondisi[i][0]
            pdf.cell(0, 5, teks_kondisi, ln=True, align='L')

        # Set width for each column (equal width)
        col_width = 15
        # Set height of the row
        row_height = 10

        # Loop through data and add cells
        for row in array_kondisi:
            for item in row:
                # Add cell
                pdf.cell(col_width, row_height, str(item), border=1)
            # Move to next line
            pdf.ln(row_height)

        teks_aksi = "R : " + act
        pdf.cell(0, 5, teks_aksi, ln=True, align='L')
        for item in arr_result:
            # Add cell
            pdf.cell(col_width, row_height, str(item), border=1)

        output_dir = Path(r"C:\Users\prade\OneDrive\Documents\Materi Kuliah\Sitasi Proposal\FINAL PROPOSAL\Api\Node-Flask-Api\RESULT")
        random_filename = ''.join(random.choices(string.ascii_letters, k=8)) + ".pdf"
        pdf.output(output_dir / random_filename)

        Result = {
            "status": "success",
            "message": "Data successfully generated.",
            "filename": random_filename
        }
        json_string = json.dumps(Result)
        return json_string

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)