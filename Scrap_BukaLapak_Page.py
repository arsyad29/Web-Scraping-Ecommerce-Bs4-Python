# Import library
from email.mime import base
from xml.dom.minidom import Attr
from bs4 import BeautifulSoup
import requests
import urllib3
import csv
import pandas as pd

# Create request
http = urllib3.PoolManager()
base_url = 'https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D=sepatu&search_source=omnisearch_keyword&source=navbar'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Input page and produk  we are looking for
produk = str(input("Input name the product: "))
j = input("Input page *(1 page = 50-100 product):")
j = int(j) + 1    

# Scraping data
datas = []
for page in range(0, j):
    req = requests.get('https://www.bukalapak.com/products?page='+str(page)+'&search%5Bkeywords%5D='+produk)
    soup = BeautifulSoup(req.text, 'html.parser')
    item_name = soup.findAll('div', attrs = {'class':'bl-flex-item mb-8'})
    for i in item_name:
        # None = Tidak diketahui
        try: Nama_produk = i.find('a', 'bl-link').text.strip().replace('\n', '').replace('Rp', '').replace('.', '')
        except: Nama_produk=None
        try: Harga = i.findAll('p')[2].text.strip().replace('\n', '').replace('Rp', '').replace('.', '')
        except: Harga=None
        try: Nama_toko = i.findAll('a')[-1].text
        except: Nama_toko=None
        try: Kota = i.find('span', 'mr-4 bl-product-card__location bl-text bl-text--body-14 bl-text--subdued bl-text--ellipsis__1').text
        except: Kota=None
        try: Rating_produk = i.find('p', 'bl-text bl-text--body-14 bl-text--subdued').text.strip()
        except: Rating_produk=None
        try: Produk_terjual = i.find_all('p', {'class':'bl-text bl-text--body-14 bl-text--subdued'})[1].text.strip().replace('Terjual', '')
        except: Produk_terjual=None
        if Nama_produk == None:
            break
        datas.append([Nama_produk, Harga, Nama_toko, Kota, Rating_produk, Produk_terjual])

# Creating file csv
kepala = ['Nama_produk', 'Harga', 'Nama_toko', 'Kota', 'Rating_produk', 'Produk_terjual']
writer = csv.writer(open('Data_Scraping_Bukalapak_Sepatu.csv', 'w', newline=''))
writer.writerow(kepala)
for d in datas: writer.writerow(d)    