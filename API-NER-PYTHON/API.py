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


app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'kuliah'
app.config['MYSQL_CHARSET'] = 'utf8mb4'
app.config['MYSQL_TIMEZONE'] = '+07:00'

mysql = MySQL(app)

TOKEN = '7027003845:AAG0MWEr0w1xSawylz4syiPDaGVc6qJV60s'
bot = Bot(token=TOKEN)


# # Inisialisasi updater
# updater = Updater(TOKEN)

# # Daftar handler
# dispatcher = updater.dispatcher

def check_index(array, value):
    try:
        return array.index(value)
    except ValueError:
        return -1
        
def result_of_logic(array):
    temp1 = []
    temp2 = []
    while (len(array) > 3):
        ind_and = check_index(array,"dan")
        if (ind_and != -1):
            for i in range(ind_and-1):
                temp1.append(array[i])
            
            for i in range(ind_and+2, len(array)):
                temp2.append(array[i])
                
            result = "True" if array[ind_and-1] == "True" and array[ind_and+1] == "True" else "False"
            temp1.append(result)
            
            array = temp1 + temp2
            temp1, temp2 = [], []
        else:
             result = "True" if array[0] == "True" or array[2] == "True" else "False"
             array.pop(0)
             array.pop(0)
             array[0] = result

    if (array[1] == "dan"):
        return "True" if array[0] == "True" and array[2] == "True" else "False"
    else:
        return "True" if array[0] == "True" or array[2] == "True" else "False"
        
def kirim_file_ke_semua(update, context, file_name):
    # Ganti dengan path file PDF yang ingin Anda kirim
    RESULTS_FOLDER_PATH = r'C:\Users\prade\OneDrive\Documents\Materi Kuliah\Sitasi Proposal\FINAL PROPOSAL\Api\Node-Flask-Api\RESULT'

    FILE_PATH = os.path.join(RESULTS_FOLDER_PATH, file_name)

    try:
        # Mengirim file kepada pengguna
        context.bot.send_document(update.effective_chat.id, open(FILE_PATH, 'rb'))
    except Exception as e:
        print(f"Gagal mengirim file kepada {update.effective_chat.id}: {e}")

# MASTER NATURAL LANGUAGE

# CREATE NATURAL LANGUAGE

@app.route('/get/ner', methods=['GET', 'POST'])
def NlpToNer():
    try:
        # nl_id = request.json['nl_id']
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
            print(arr)
            result = []
            max_length = max(len(arr), len(array_gate))
            print(max_length)

            for i in range(max_length):
                print(2)
                if i < len(arr):
                    print(3)
                    result.append(arr[i])
                if i < len(array_gate):
                    print(4)
                    result.append(array_gate[i])
            print(result, result_of_logic(result))
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
        # pdf_output_path = output_dir / random_filename

        chat_id = "-1002048819241"

        bot.send_document(chat_id=chat_id, document=open(f"C:/Users/prade/OneDrive/Documents/Materi Kuliah/Sitasi Proposal/FINAL PROPOSAL/Api/Node-Flask-Api/RESULT/{random_filename}", 'rb'))

        # url = f"http://192.168.12.239:8000/send/tele/{random_filename}"

        # response = requests.get(url)

        # print(response)



        Result = {
            "status": "success",
            "message": "Data successfully generated.",
            "filename": random_filename
        }
        json_string = json.dumps(Result)
        return json_string
        # return send_file(pdf_output_path, as_attachment=True)



    except Exception as e:
        return str(e), 500
    
# @app.route('/send/tele/<filename>', methods=['GET', 'POST'])
# def send_to_tele(filename):
#     try:

#         # Menambahkan handler untuk perintah /kirimfile
#         dispatcher.add_handler(CommandHandler('ambiltestcase', lambda update, context: kirim_file_ke_semua(update, context, filename)))

#         # Mulai polling
#         updater.start_polling()

#         updater.idle()
#         dispatcher.remove_handler('/ambiltestcase')
#         # time.sleep(30)
#         # # Menutup program saat pengguna menekan Ctrl+C
#         # updater.stop()
        

#         return "Success"
    # except Exception as e:
    #     return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
