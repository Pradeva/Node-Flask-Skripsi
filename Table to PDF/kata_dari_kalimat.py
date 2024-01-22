kalimat = "apple lebih dari 10 dan kuas lebih dari 3"
kata_cari = "kutu"

posisi_awal = kalimat.find(kata_cari)

if posisi_awal != -1:
    panjang_kata = len(kata_cari)
    posisi_akhir = posisi_awal + panjang_kata - 1
    print(f"Kata '{kata_cari}' ditemukan pada posisi: {posisi_awal} - {posisi_akhir}")
else:
    print(f"Kata '{kata_cari}' tidak ditemukan dalam kalimat.")
