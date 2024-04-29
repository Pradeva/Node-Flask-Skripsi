kalimat = "apple lebih dari 10 dan kuas lebih dari 3"
kata_cari = "apple"

posisi_awal = kalimat.find(kata_cari)
print(kalimat[0:7])

if posisi_awal != -1:
    panjang_kata = len(kata_cari)
    posisi_akhir = posisi_awal + panjang_kata
    print(f"Kata '{kata_cari}' ditemukan pada posisi: {posisi_awal} - {posisi_akhir}")
    print(kalimat)
else:
    print(f"Kata '{kata_cari}' tidak ditemukan dalam kalimat.")
