# Import library
from email.mime import base
from xml.dom.minidom import Attr
from bs4 import BeautifulSoup
import requests
import urllib3
import csv

# Create request
http = urllib3.PoolManager()
base_url = 'https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D=sepatu&search_source=omnisearch_keyword&source=navbar'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Get request
# req  = requests.get(base_url, headers=headers)
# soup = BeautifulSoup(req.text, 'html.parser')

# Input produk yang ingin di cari
produk = str(input("Masukkan nama produk: "))

# Scraping data
datas = []
j = input("Masukkan jumlah halaman yang ingin di ambil *(1 page = 50 product):")
j = int(j) + 1    
for page in range(0, j):
    req = requests.get('https://www.bukalapak.com/products?page='+str(page)+'&search%5Bkeywords%5D='+produk)
    soup = BeautifulSoup(req.text, 'html.parser')
    item_name = soup.findAll('div', attrs = {'class':'bl-flex-item mb-8'})
    for i in item_name:
        try: Nama_produk = i.find('a', 'bl-link').text.strip().replace('\n', '').replace('Rp', '').replace('.', '')
        except: Nama_produk=''
        try: Harga = i.findAll('p')[2].text.strip().replace('\n', '').replace('Rp', '').replace('.', '')
        except: Harga=''
        try: Nama_toko = i.findAll('a')[-1].text
        except: Nama_toko=''
        try: Kota = i.find('span', 'mr-4 bl-product-card__location bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1').text
        except: Kota=''
        try: Rating_produk = i.find('p', 'bl-text bl-text--body-14 bl-text--subdued').text.strip()
        # None = Tidak diketahui
        except: Rating_produk=None
        try: Produk_terjual = i.find_all('p', {'class':'bl-text bl-text--body-14 bl-text--subdued'})[1].text.strip().replace('Terjual', '')
        except: Produk_terjual=None
        # print(terjual)
        datas.append([Nama_produk, Harga, Nama_toko, Kota, Rating_produk, Produk_terjual])

print(datas)
# Creating file csv
# kepala = ['Nama_produk', 'Harga', 'Nama_toko', 'Kota', 'Rating_produk', 'Produk_terjual']
# writer = csv.writer(open('Data_Scraping_Bukalapak_Sepatu.csv', 'w', newline=''))
# writer.writerow(kepala)
# for d in datas: writer.writerow(d)    