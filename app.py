import requests
from bs4 import BeautifulSoup
import csv
import time

# URL halaman utama produk
url = 'https://www.tissueku.com/tissue/tissue-facial'

html_doc = '''<div class="woocommerce-product-details__short-description"><h3>Info Tissue Facial See U 600 Gram</h3><p>Tisu Facial See U 600 Gram 1 dus : 20 pcs</p><hr></div>'''
soup2 = BeautifulSoup(html_doc, 'html.parser')

# Mengirim permintaan HTTP GET ke halaman utama
response = requests.get(url)

# Memeriksa apakah permintaan berhasil
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    data_produk = []

    # Mengambil semua elemen produk yang diinginkan
    produk_items = soup.find_all('div',
                                 class_='jet-woo-products__item jet-woo-builder-product col-desk-4 col-tab-3 col-mob-2')

    for item in produk_items:
        # Mendapatkan judul produk
        title = item.find('h5', class_='jet-woo-product-title')
        title_text = title.get_text(strip=True) if title else "N/A"

        # Mendapatkan harga produk
        price = item.find('span', class_='woocommerce-Price-amount amount')
        price_text = price.get_text(strip=True) if price else "N/A"

        # Mendapatkan link ke halaman detail
        detail_link = item.find('a', href=True)
        detail_url = detail_link['href'] if detail_link else None

        # Mengambil deskripsi dan informasi tambahan dari halaman detail
        description_text = "N/A"
        additional_info_text = "N/A"

        if detail_url:
            detail_response = requests.get(detail_url)

            if detail_response.status_code == 200:
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

                # Mengambil deskripsi produk
                description = soup2.find('div', class_='woocommerce-product-details__short-description').find(text=True, recursive=False).strip()
                description_text = description.get_text(strip=True) if description else "N/A"

                print(description)

                # Jeda untuk menghindari blokir
                time.sleep(1)

        # Menyimpan informasi produk ke dalam list
        data_produk.append([title_text, price_text, description_text])

    # Menyimpan data ke CSV
    with open('hasil_scraping_dengan_detail.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Judul', 'Harga', 'Quantity'])
        writer.writerows(data_produk)

    print("Data berhasil disimpan ke hasil_scraping_dengan_detail.csv")
else:
    print(f"Gagal mengakses halaman utama: {response.status_code}")
