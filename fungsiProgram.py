from collections import defaultdict
from math import ceil
import Linkedlist
from random import choice
from datetime import datetime
from locale import setlocale, LC_TIME

lk = Linkedlist.Linkedlist()

class fungsiProgram:
    def fungsiDataMakanan(self, namaFile):
        dataMakanan = []

        with open(namaFile, 'r') as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                data = line.split('|')

                makanan = data[0]
                kategori = data[1]
                harga = int(data[2])
                diskon = int(float(data[3]) * 100) 
                gambar = data[4]
                deskripsi = data[5]

                # Format harga menjadi nilai rupiah
                harga_rupiah = "Rp {:,}".format(harga).replace(',', '.')

                dataMakanan.append([makanan, kategori, harga, diskon, gambar, harga_rupiah, deskripsi])
        return dataMakanan

    def fungsiDataKategori(self, dataMakanan):
        kategori_harga = defaultdict(list)

        for makanan in dataMakanan:
            kategori = makanan[1]
            harga = makanan[2]
            gambar = makanan[4]

            kategori_harga[kategori].append((harga, gambar))

        return kategori_harga

    # Fungsi untuk menghitung harga total kategori makanan
    def fungsiRataRataKategori(self, kategori_harga):
        harga_total = []

        for kategori, harga_list in kategori_harga.items():
            total_duplikat = len(harga_list)
            total_harga = sum(harga for harga, _ in harga_list)
            rata_rata_harga = total_harga / total_duplikat
            harga_total.append((kategori, ceil(rata_rata_harga / 500) * 500, harga_list[0][1], total_duplikat))
        return harga_total

    def fungsiDataPesananOriginal(self):
        return lk.ambilData()
    
    def fungsiDataPesananKonversi(self, dataPesanan, dataMakanan):
        data = []
        for index, isi in enumerate(dataPesanan):
            nama = isi[0]
            jumlah = isi[1]
            total, harga = self.fungsiHargaMakanan(nama, jumlah, dataMakanan)
            
            item = [nama, jumlah, total, harga]
            data.append(item)
        print(data)
        return data
        
    def fungsiHapusPesanan(self, nama):
        lk.hapusData(nama)

    def fungsiTambahPesanan(self, namaPesanan, jumlahPesanan):
        self.namaPesanan = namaPesanan
        self.jumlahPesanan = int(jumlahPesanan)

        lk.tambahData(self.namaPesanan, self.jumlahPesanan)
        
        
    def fungsiCariMenu(self, dataMakanan, nama):
        menu = None
        for data_menu in dataMakanan:
            if data_menu[0] == nama:
                menu = data_menu
                break
        return menu
    
    def fungsiHargaMakanan(self, nama, jumlah, dataMakanan):
        total = 0
        for makanan in dataMakanan:
            if makanan[0] == nama:
                # print(f"{makanan[0]}, {nama}")
                total = int(makanan[2]) * int(jumlah)
                return total, int(makanan[2])

    def fungsiSubTotalPesanan(self, dataMakanan, dataPesanan):
        total_harga = 0
        total_diskon = 0
        for item in dataPesanan:
            nama_menu = item[0]
            jumlah = int(item[1])
            
            menu = self.fungsiCariMenu(dataMakanan, nama_menu)
            
            if menu:
                harga = int(menu[2])
                diskon = float(menu[3]) / 100
                harga_diskon = harga * (1 - diskon)
                # print(harga_diskon)
                total_diskon += (harga_diskon * jumlah)
                total_harga += (harga * jumlah)
            else:
                print(f"Menu {nama_menu} tidak ditemukan.")
        total_diskon = total_harga - total_diskon
        return total_harga, total_diskon

    def fungsiKodeUnik(self):
        code = ''
        digits = '0123456789'
        
        for _ in range(8):
            code += choice(digits)
        return code
    
    def fungsiWaktu(self):
        setlocale(LC_TIME, 'id_ID')
        x = datetime.now()
        waktu = x.strftime("%A %x")
        jam = x.strftime("%H:%M")

        return waktu, jam
    
    def fungsiHapusSemuaPesanan(self):
        lk.hapusSemuaData()

    def fungsiFilterMakanan(self, dataMakanan, kategoriFilter, diskon):
        hasilFilter = []

        for makanan in dataMakanan:
            kategori = makanan[1]
            diskonMakanan = makanan[3]
            if not diskon and kategoriFilter:  # Jika diskon kosong, artinya tidak ada filter diskon
                if kategori in kategoriFilter:
                    hasilFilter.append(makanan)
            elif not kategoriFilter and diskon:
                for dis in diskon:
                    diskonMin = int(dis)
                    diskonMax = int(dis) + 4
                    print(diskonMin)
                    if diskonMin <= diskonMakanan <= diskonMax:
                        hasilFilter.append(makanan)
            elif not kategoriFilter and not diskon:
                hasilFilter.append(makanan)
            else:
                for dis in diskon:
                    diskonMin = int(dis)
                    diskonMax = int(dis) + 4
                    print(diskonMin)
                    if kategori in kategoriFilter and diskonMin <= diskonMakanan <= diskonMax:
                        hasilFilter.append(makanan)
                        
        return hasilFilter