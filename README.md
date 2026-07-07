# 🍌 Banana Classification

Sistem klasifikasi tingkat kematangan buah pisang berbasis **Computer Vision** menggunakan **YOLOv8 Classification** dan **Flask**. Aplikasi ini mampu mendeteksi apakah gambar merupakan buah pisang, kemudian mengklasifikasikan tingkat kematangannya menjadi **Mentah**, **Setengah Matang**, atau **Matang**.

---

## 📌 Fitur

- Deteksi objek pisang sebelum proses klasifikasi.
- Klasifikasi tingkat kematangan buah pisang.
- Menampilkan nilai confidence hasil prediksi.
- Menampilkan seluruh probabilitas setiap kelas.
- Menampilkan nilai rata-rata RGB pada Region of Interest (ROI).
- Visualisasi area fokus (ROI) pada bagian tengah buah pisang.
- Antarmuka web sederhana menggunakan Flask.

---

## 🖼️ Hasil Klasifikasi

Alur kerja sistem:

1. Upload gambar.
2. Sistem mendeteksi apakah terdapat objek pisang.
3. Sistem menentukan Region of Interest (ROI) pada bagian tengah buah.
4. Menghitung nilai rata-rata RGB dari ROI.
5. Model YOLOv8 melakukan klasifikasi tingkat kematangan.
6. Menampilkan hasil prediksi beserta confidence.

---

## 📂 Struktur Project

```
banana-classification/
│
├── dataset/                  # Dataset training
├── model/                    # Model YOLO
│   ├── klasifikasi_pisang.pt
│   └── yolov8n_deteksi_pisang_non_pisang.pt
│
├── static/
│
├── templates/
│   └── index.html
│
├── upload/                   # Folder penyimpanan gambar upload
│
├── app.py                    # Program utama Flask
├── requirements.txt          # Library Python
├── train_model.ipynb         # Notebook training model
└── README.md
```

---

## 🧠 Arsitektur Sistem

```
Input Gambar
      │
      ▼
Deteksi Objek Pisang (YOLOv8 Detection)
      │
      ▼
Region of Interest (ROI)
      │
      ▼
Ekstraksi Nilai RGB
      │
      ▼
YOLOv8 Classification
      │
      ▼
Hasil Klasifikasi
```

---

## 📊 Kelas Kematangan

Model mengenali tiga kelas:

| Label | Keterangan |
|--------|------------|
| 🌿 Mentah | Kulit buah masih didominasi warna hijau |
| 🍃 Setengah Matang | Warna hijau dan kuning mulai seimbang |
| 🍌 Matang | Kulit buah didominasi warna kuning |

---

## 🛠️ Teknologi yang Digunakan

- Python 3
- Flask
- OpenCV
- NumPy
- Ultralytics YOLOv8
- HTML
- CSS
- JavaScript

---

## 📦 Instalasi

Clone repository

```bash
git clone https://github.com/username/banana-classification.git
```

Masuk ke folder project

```bash
cd banana-classification
```

Install dependency

```bash
pip install -r requirements.txt
```

---

## 📁 Download Model

Project ini memerlukan dua model YOLO yang harus diletakkan pada folder:

```
model/
```

Struktur folder:

```
model/
├── klasifikasi_pisang.pt
└── yolov8n_deteksi_pisang_non_pisang.pt
```

---

## ▶️ Menjalankan Program

```bash
python app.py
```

Kemudian buka browser

```
http://127.0.0.1:5000
```

---

## 🔍 Cara Kerja

### 1. Upload Gambar

Pengguna mengunggah gambar buah pisang.

---

### 2. Deteksi Pisang

Model YOLO melakukan deteksi objek untuk memastikan gambar benar-benar berisi buah pisang.

Jika tidak ditemukan objek pisang, sistem akan menampilkan pesan:

```
Bukan Pisang
```

---

### 3. Region of Interest (ROI)

Apabila pisang berhasil dideteksi, sistem mengambil area fokus pada bagian tengah buah menggunakan bounding box yang diperkecil.

ROI digunakan untuk:

- mengurangi pengaruh background
- mengurangi noise
- memperoleh warna kulit pisang yang lebih representatif

---

### 4. Ekstraksi RGB

Sistem menghitung nilai rata-rata:

- Red (R)
- Green (G)
- Blue (B)

dari area ROI menggunakan OpenCV.

---

### 5. Klasifikasi

Model YOLOv8 Classification memprediksi tingkat kematangan menjadi:

- Mentah
- Setengah Matang
- Matang

---

### 6. Output

Sistem menampilkan:

- hasil klasifikasi
- confidence (%)
- probabilitas setiap kelas
- nilai RGB ROI
- gambar dengan area fokus

---

## 📸 Contoh Output

```
Prediksi :
🍌 Matang

Confidence :
98.74%

RGB
R : 201.5
G : 182.3
B : 64.1
```

---

## 📚 Dataset

Dataset terdiri dari tiga kategori:

- Mentah
- Setengah Matang
- Matang

Dataset digunakan untuk proses pelatihan model klasifikasi menggunakan YOLOv8 Classification.

---

## 📈 Model

Model klasifikasi:

```
YOLOv8 Classification
```

Model deteksi:

```
YOLOv8 Detection
```

---

## 👨‍💻 Author

**Laode Farhan Fadilah**

Teknik Informatika

Universitas Borobudur Jakarta

---

## 📄 Lisensi

Project ini dibuat untuk keperluan penelitian dan tugas akhir (skripsi). Silakan gunakan sebagai referensi dengan tetap mencantumkan sumber apabila digunakan dalam penelitian atau pengembangan lebih lanjut.
