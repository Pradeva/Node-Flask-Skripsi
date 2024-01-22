from fpdf import FPDF
from pathlib import Path

# Data untuk tabel pertama
TABLE_DATA_1 = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Carlson", "Banks", "19", "Los Angeles"),
    ("Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire"),
)

# Data untuk tabel kedua
TABLE_DATA_2 = (
    ("ID", "Product", "Price"),
    ('1', "Laptop", '1200'),
    ('2', "Smartphone", '800'),
    ('3', "Tablet", '400'),
    ('4', "Headphones", '150'),
    ('5', "Camera", '600'),
    ('6', "Printer", '300'),
    ('7', "Monitor", '500'),
    ('8', "Keyboard", '80'),
    ('9', "Mouse", '40'),
    ('10', "Speaker", '120'),
)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size=16)

teks_atas = 'Informasi Penduduk'

# Tambahkan teks di atas tabel pertama
pdf.set_xy(10, 10)
pdf.cell(0, 10, teks_atas, ln=True, align='L')

# Buat tabel pertama
pdf.set_fill_color(200, 220, 255)
pdf.set_text_color(0, 0, 0)
pdf.set_draw_color(0, 0, 0)
pdf.set_line_width(0.3)

# Judul kolom tabel pertama
col_widths_1 = [pdf.get_string_width(str(max(data, key=len))) + 6 for data in zip(*TABLE_DATA_1)]
pdf.set_font("Times", size=12)
for i, col_name in enumerate(TABLE_DATA_1[0]):
    pdf.cell(col_widths_1[i], 10, col_name, 1)

pdf.ln()

# Isi tabel pertama
pdf.set_font("Times", size=12)
for data_row in TABLE_DATA_1[1:]:
    for i, datum in enumerate(data_row):
        pdf.cell(col_widths_1[i], 10, str(datum), 1)
    pdf.ln()

# Tambahkan teks di bawah tabel pertama
teks_bawah_1 = 'Tabel ini berisi informasi tentang beberapa penduduk.'
pdf.cell(0, 10, teks_bawah_1, ln=True, align='L')

# Buat tabel kedua
pdf.ln(10)  # Jarak antara teks bawah tabel pertama dan tabel kedua
pdf.set_fill_color(200, 220, 255)
pdf.set_text_color(0, 0, 0)
pdf.set_draw_color(0, 0, 0)
pdf.set_line_width(0.3)

# Judul kolom tabel kedua
col_widths_2 = [pdf.get_string_width(str(max(data, key=len))) + 6 for data in zip(*TABLE_DATA_2)]
pdf.set_font("Times", size=12)
for i, col_name in enumerate(TABLE_DATA_2[0]):
    pdf.cell(col_widths_2[i], 10, col_name, 1)

pdf.ln()

# Isi tabel kedua
pdf.set_font("Times", size=12)
for data_row in TABLE_DATA_2[1:]:
    for i, datum in enumerate(data_row):
        pdf.cell(col_widths_2[i], 10, str(datum), 1)
    pdf.ln()

output_dir = Path(r"C:\Users\prade\OneDrive\Documents\Materi Kuliah\Sitasi Proposal\FINAL PROPOSAL\Node-Flask-Api\RESULT")

pdf.output(output_dir / 'tables.pdf')

# C:\Users\prade\OneDrive\Documents\Materi Kuliah\Sitasi Proposal\FINAL PROPOSAL\Node-Flask-Api\RESULT
