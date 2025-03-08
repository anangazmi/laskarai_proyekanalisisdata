# 📊 Dashboard Analisis Data E-Commerce  

## 📌 Deskripsi Proyek  
Proyek ini adalah **dashboard interaktif** berbasis **Streamlit** untuk menganalisis data e-commerce.  
Dashboard ini memungkinkan pengguna untuk:  
✅ **Mengetahui produk terlaris** dalam periode tertentu  
✅ **Menganalisis metode pembayaran** yang paling sering digunakan  
✅ **Menampilkan kota dan negara bagian** dengan pesanan terbanyak  
✅ **Mengamati rata-rata waktu pengiriman** per kategori produk  
✅ **Menganalisis tren penjualan** berdasarkan bulan  

---

## 📂 Struktur Folder  
```
 📦 proyek-dashboard
┣ 📂 dashboard
┃ ┣ 📜 dashboard.py
┃ ┣ 📜 all_data.csv
┣ 📂 data
┃ ┣ 📜 customers_dataset.csv
┃ ┣ 📜 geolocation_dataset.csv
┃ ┣ 📜 order_items_dataset.csv
┃ ┣ 📜 order_payments_dataset.csv
┃ ┣ 📜 order_reviews_dataset.csv
┃ ┣ 📜 orders_dataset.csv
┃ ┣ 📜 product_category_name_translation.csv
┃ ┣ 📜 products_dataset.csv
┃ ┣ 📜 sellers_dataset.csv
┣ 📜 notebook.py
┣ 📜 README.md
┣ 📜 requirements.txt
```
---
## 🛠️ Setup Environment  

### 📌 1. Menggunakan **Anaconda**  
#### 1️⃣ Buka Anaconda Prompt  
#### 2️⃣ Buat environment baru:  
   ```
   conda create -n ecommerce-dashboard python=3.10
   ```
#### 3️⃣ Aktifkan environment:
  ```
  conda activate ecommerce-dashboard
  ```
#### 4️⃣ Install dependensi:
  ```
  pip install -r requirements.txt
  ```

---

### 📌 2. Menggunakan Shell/Terminal
#### 1️⃣ Pastikan Python 3.10 sudah terinstall, lalu buat virtual environment:
```
python -m venv ecommerce-dashboard
```
#### 2️⃣ Aktifkan virtual environment:
###### Windows:
```
ecommerce-dashboard\Scripts\activate
```
##### Mac/Linux:
```
source ecommerce-dashboard/bin/activate
```

#### 3️⃣ Install dependensi:
```
pip install -r requirements.txt
```

---

### 🚀 Menjalankan Aplikasi Streamlit
#### 🔹 Dari Local Machine
Setelah semua setup selesai, jalankan perintah berikut:
```
cd dashboard
streamlit run dashboard.py
```
Kemudian, buka browser dan akses http://localhost:8501 untuk melihat dashboard interaktif. 🎉
#### 🔹 Dari GitHub (Streamlit Cloud)
Untuk menjalankan aplikasi langsung dari GitHub, ikuti langkah berikut:
##### 1️⃣ Fork repository ini ke akun GitHub Anda
##### 2️⃣ Buka Streamlit Cloud → https://share.streamlit.io/
##### 3️⃣ Login dengan akun GitHub
##### 4️⃣ Klik "New App", lalu pilih repository yang sudah di-fork
##### 5️⃣ Atur path file utama:
```
dashboard/dashboard.py
```
##### 6️⃣ Klik "Deploy", tunggu proses selesai, dan akses aplikasi Anda! 🚀

---

## 📢 Kontak
#### 📧 Email: A163YAF089@devacademy.id
#### 👨‍💻 Dibuat oleh: Azmi Irfala