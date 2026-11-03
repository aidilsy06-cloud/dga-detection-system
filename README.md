# SISTEM DETEKSI DOMAIN GENERATION ALGORITHM (DGA) BERBASIS MACHINE LEARNING
**Platform Keamanan Siber Cerdas (Intelligent Cyber Security Platform)**

---

## 1. Tinjauan Umum Sistem
Sistem Deteksi DGA adalah sebuah platform keamanan siber cerdas (*intelligent cyber security platform*) yang dirancang untuk mengidentifikasi dan memutus jalur komunikasi malware ke server Command and Control (C2). Sistem ini bekerja secara *real-time* atau *batch* dengan menganalisis kueri Domain Name System (DNS) menggunakan algoritma Machine Learning, khususnya **Random Forest Classifier**, untuk membedakan antara domain operasional sah (*Legit*) dan domain hasil komputasi algoritma (*DGA*).

Sistem dibangun dengan arsitektur berbasis web yang memisahkan hak akses antara analis keamanan (*Security Analyst*) di sisi Front-End dan administrator sistem di sisi Back-End.

---

## 2. Alur Implementasi dan Cara Kerja Sistem (*End-to-End Pipeline*)
1. **Pengumpulan Data (*Data Ingestion*):** Sistem menangkap kueri DNS dari pengguna jaringan secara live streaming atau menerima unggahan file log DNS (CSV/TXT/PCAP-log).
2. **Ekstraksi Fitur Leksikal (*Feature Engineering*):**
   - **Panjang Domain (*Domain Length*):** Jumlah total karakter domain.
   - **Rasio Huruf Vokal (*Vowel Ratio*):** Frekuensi huruf `a, e, i, o, u` terhadap panjang domain.
   - **Rasio Angka (*Digit Ratio*):** Frekuensi angka `0-9` terhadap panjang domain.
   - **Entropi Shannon (*Shannon Entropy*):** Formula derajat keacakan karakter $H(X) = -\sum P(x_i) \log_2 P(x_i)$.
3. **Klasifikasi Machine Learning (*Inference*):**
   Fitur yang telah diekstraksi dinormalisasi via `StandardScaler` dan dimasukkan ke dalam model **Random Forest Classifier**. Model menghasilkan probabilitas prediksi $P(\text{DGA})$. Jika probabilitas melampaui ambang batas keputusan (**threshold optimal: 0.40 – 0.42**), domain diklasifikasikan sebagai ancaman DGA.
4. **Tindakan Mitigasi (*Action/Response*):**
   Domain DGA secara otomatis dicatat dalam *Immutable Audit Log*, dimasukkan ke daftar cekal, diekspor ke aturan Firewall (IPTables/pfSense), atau dialihkan ke **DNS Sinkhole (IP: 10.10.10.254)**.

---

## 3. Rincian Fitur Antarmuka Pengguna (Front-End - SOC Analyst)
- **Dashboard Utama (*Executive Overview*):**
  - Ringkasan metrik harian (Total DNS Queries, Ancaman DGA, Domain Sah, Tingkat Ancaman Jaringan).
  - Grafik visual tren lalu lintas DNS (24 Jam) menggunakan Chart.js.
  - Diagram rasio distribusi domain sah vs DGA.
  - Tabel investigasi temuan insiden DGA terkini.
- **Single Domain Scanner (*Pemindai Mandiri*):**
  - Uji cepat satu nama domain (FQDN).
  - Menampilkan 4 fitur leksikal, confidence score, probabilitas DGA, dan status mitigasi.
  - Dilengkapi tombol sampel uji instan (Legit & DGA).
- **Batch Upload Inspection (*Inspeksi Log Massal*):**
  - Pengunggahan file log jaringan (CSV, TXT, LOG, Excel).
  - Ringkasan statistik ancaman file.
  - Tabel dinamis dengan filter interaktif (*Semua / Hanya DGA / Hanya Legit*) dan pencarian nama domain.
  - Unduh **Laporan Investigasi Resmi (Format PDF & Cetak)** serta ekspor CSV.
- **Real-Time DNS Log Stream:**
  - Pemantauan kronologis kueri DNS aktif.
  - Kolom: Stempel Waktu, IP Sumber, Nama Domain, Skor Entropi, Probabilitas, dan Status Tindakan (*Izinkan / Blokir-Sinkhole*).
  - Tombol kontrol: Pause/Resume Stream, Pembersihan Tampilan, dan **Simulasi Traffic Masuk**.

---

## 4. Rincian Fitur Administrator (Back-End)
- **Model Management & Evaluation Metrics:**
  - Evaluasi metrik kualitas model Random Forest aktif:
    - **Akurasi:** 87,59%
    - **Presisi:** 93,79%
    - **Recall (Sensitivitas):** 80,51%
    - **F1-Score:** 86,64%
  - Visualisasi 2x2 **Confusion Matrix**:
    - True Positive (TP): 665
    - False Positive (FP): 44
    - False Negative (FN): 161
    - True Negative (TN): 782
  - Diagram kontribusi fitur (*Feature Importance* / Gini Importance).
- **Decision Threshold Tuning:**
  - Slider interaktif (0.10 – 0.90) untuk mengatur sensitivitas deteksi secara langsung tanpa perlu melatih ulang model.
  - Penanda visual zona optimal (0.40 – 0.42).
- **Firewall & DNS Sinkhole Integration:**
  - Konfigurasi IP target DNS Sinkhole (default: `10.10.10.254`).
  - Sinkronisasi aturan perimeter dengan 1-klik.
  - Ekspor aturan dalam 4 format:
    1. Linux IPTables (`.sh`)
    2. BIND9 / RPZ Policy Zone (`.zone`)
    3. OS Hosts File (`0.0.0.0 domain`)
    4. pfSense / Fortinet URL Table (`.txt`)
  - Whitelist / unblock domain.
- **Dataset Management & Retraining Pipeline:**
  - Ringkasan korpus dataset (Total sampel, Legit, DGA).
  - Pengunggahan dataset baru (CSV / Excel).
  - Tombol picu siklus pelatihan ulang (*Trigger Retraining Pipeline*) dengan pembaruan metrik seketika.
- **API & Webhook Management:**
  - Pembuatan dan pencabutan API Key (`X-API-Key`).
  - Endpoint REST API publik (`POST /api/v1/detect`).
  - Konfigurasi Webhook ke Discord Channel / Telegram Bot dengan tombol uji coba (*Test Alert*).
- **System Health & Infrastructure Monitoring:**
  - Pemantauan perangkat keras server: Utilisasi CPU (%), RAM (GB), dan Disk (GB).
  - Latensi inferensi model (*sub-millisecond latency ~1.2 ms*).
  - Status modul operasional (*DNS Ingestion, ML Pipeline, Database, Firewall Sync*).
- **User Access Control & Audit Trail (RBAC):**
  - Manajemen peran (*Role-Based Access Control*): Security Analyst vs Administrator.
  - Log aktivitas tidak dapat diubah (*Immutable Audit Trail*) mencatat waktu, user, aksi, rincian, dan IP klien.

---

## 5. Cara Menjalankan Sistem
1. Pastikan dependensi terpasang:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi web:
   ```bash
   cd "Penentuan Bantuan"
   python app.py
   ```
   *(Atau klik ganda file `run.bat` di folder utama)*
3. Buka peramban (*browser*) pada alamat:
   ```
   http://127.0.0.1:5000
   ```
4. Anda dapat berpindah peran antara **Security Analyst** dan **Administrator** kapan saja menggunakan tombol *Role Switcher* di pojok kanan atas navigasi.
