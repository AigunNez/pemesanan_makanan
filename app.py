from flask import Flask, render_template, request, url_for, redirect
import fungsiProgram

app = Flask(__name__)
fp = fungsiProgram.fungsiProgram()

namaFile = "data/dataMakanan.txt"
    
menuMakanan = fp.fungsiDataMakanan(namaFile)
kategoriMakanan = fp.fungsiDataKategori(menuMakanan)
dataKategori = fp.fungsiRataRataKategori(kategoriMakanan)

@app.route("/")
def main():
    menuMakanan1 = menuMakanan[:7]
    menuMakanan2 = menuMakanan[7:14]
    
    return render_template("home.html", dataKategori=dataKategori, menuMakanan1=menuMakanan1, menuMakanan2=menuMakanan2)

@app.route("/menu_makanan", methods=['GET','POST'])
def menu():
    if "tambahPesanan" in request.form:
        namaPesanan = request.form['nama']
        jumlahPesanan = request.form['jumlah']
        
        fp.fungsiTambahPesanan(namaPesanan, jumlahPesanan)
    elif "hapusPesanan" in request.form:
        namaHapus = request.form['namaHapus']
        fp.fungsiHapusPesanan(namaHapus)
        
    dataPesananOriginal = fp.fungsiDataPesananOriginal()
    subTotal, diskon = fp.fungsiSubTotalPesanan(menuMakanan, dataPesananOriginal)
    dataPesananKonversi = fp.fungsiDataPesananKonversi(dataPesananOriginal, menuMakanan)
    total = subTotal + 1000 - diskon
    
    panjangKategori = int(len(dataKategori) / 2)
    kategori1 = dataKategori[panjangKategori:]
    kategori2 = dataKategori[:panjangKategori]
    
    if "filter" in request.form:
        if "kategori2" in request.form:
            filterMakanan =[request.form['kategori2']]
        else :
            print(request.form.getlist('kategori'))
            filterMakanan = request.form.getlist('kategori')
        disk = request.form.getlist('diskon')
        dataFilter = fp.fungsiFilterMakanan(menuMakanan, filterMakanan, disk)
        return render_template("menu_makanan.html", menuMakanan=dataFilter, dataPesanan=dataPesananKonversi, subTotal=subTotal, total=total, kategori1=kategori1, kategori2=kategori2, diskon=int(diskon))    

    return render_template("menu_makanan.html", menuMakanan=menuMakanan, dataPesanan=dataPesananKonversi, subTotal=subTotal, total=total, kategori1=kategori1, kategori2=kategori2, diskon=int(diskon))

@app.route("/pembayaran")
def pembayaran():
    dataPesananOriginal = fp.fungsiDataPesananOriginal()

    subTotal, diskon = fp.fungsiSubTotalPesanan(menuMakanan, dataPesananOriginal)
    dataPesananKonversi = fp.fungsiDataPesananKonversi(dataPesananOriginal, menuMakanan)
    # print(dataPesananKonversi)
    total = subTotal + 1000 - diskon
    
    if len(dataPesananOriginal) == 0:
        return redirect(url_for('menu'))
    
    waktu, jam = fp.fungsiWaktu()
    
    return render_template("pembayaran.html", dataPesanan=dataPesananKonversi, subTotal=subTotal, total=total, waktu=waktu, jam=jam, diskon=int(diskon))

@app.route("/struk_pembayaran", methods=['GET','POST'])
def struk():

    nama = request.form['nama_lengkap']
    metode = request.form['payment_method']
    if metode == " ":
        metodePembayaran = "Kartu Kredit"
    else :
        metodePembayaran = "Uang Tunai"

    dataPesananOriginal = fp.fungsiDataPesananOriginal()
    subTotal, diskon = fp.fungsiSubTotalPesanan(menuMakanan, dataPesananOriginal)
    dataPesananKonversi = fp.fungsiDataPesananKonversi(dataPesananOriginal, menuMakanan)
    total = subTotal + 1000 - diskon
    kodeUnik = fp.fungsiKodeUnik()
    
    waktu, jam = fp.fungsiWaktu()
    
    if len(dataPesananOriginal) == 0:
        return redirect(url_for('menu'))
    
    if "jumlah_bayar" in request.form:  
        bayaran = request.form['jumlah_bayar']
        fp.fungsiHapusSemuaPesanan()
        return render_template("struk.html", nama=nama, dataPesanan=dataPesananKonversi, subTotal=subTotal, total=total, kodeUnik=kodeUnik, metodePembayaran=metodePembayaran, bayaran=bayaran, waktu=waktu, diskon=int(diskon)) 
    
    fp.fungsiHapusSemuaPesanan()
    return render_template("struk.html", dataPesanan=dataPesananKonversi, subTotal=subTotal, total=total, kodeUnik=kodeUnik, diskon=int(diskon)) 

if __name__ == "__main__":
    app.run(debug=True)