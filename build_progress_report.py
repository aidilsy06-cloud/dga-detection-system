import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'doc_assets')
DOCX_OUT = os.path.join(BASE_DIR, 'Laporan_Progress_Sistem_Deteksi_DGA.docx')
DOCX_OUT_EXTRA = os.path.join(BASE_DIR, 'Laporan_Progress_Sistem_Deteksi_DGA_Rapi_Lengkap.docx')

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_with_spacing(doc, text, level=1, before=14, after=6):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(before)
    h.paragraph_format.space_after = Pt(after)
    return h

def add_caption(doc, text, c_color):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.italic = True
    r.font.color.rgb = c_color
    return p

def create_report():
    doc = docx.Document()

    # Standard Margins (1 inch / 2.54 cm all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette
    c_primary = RGBColor(15, 23, 42)    # Slate 900
    c_blue = RGBColor(2, 132, 199)      # Sky 600
    c_dark_blue = RGBColor(37, 99, 235) # Blue 600
    c_slate = RGBColor(71, 85, 105)     # Slate 600
    c_text = RGBColor(30, 41, 59)       # Slate 800

    # ---------------------------------------------------------
    # COVER / HEADER
    # ---------------------------------------------------------
    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_badge = p_badge.add_run("LAPORAN PROGRESS TUGAS KELOMPOK PROYEK REKAYASA SISTEM")
    run_badge.font.name = "Arial"
    run_badge.font.size = Pt(10)
    run_badge.font.bold = True
    run_badge.font.color.rgb = c_blue

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(6)
    run_title = p_title.add_run("SISTEM DETEKSI DOMAIN GENERATION ALGORITHM (DGA)\nBERBASIS MACHINE LEARNING")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = c_primary

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("Platform Keamanan Siber Cerdas untuk Deteksi & Mitigasi Jalur Komunikasi Malware Command and Control (C2)")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(10)
    run_sub.font.color.rgb = c_slate

    # Metadata Table with Group Members
    tbl_meta = doc.add_table(rows=6, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False

    meta_info = [
        ("Nama Anggota Kelompok", "1. Priska Liza Utami\n2. Warda Widya Ningsih\n3. Mhd. Aidil Syahron"),
        ("Topik Proyek", "Sistem Keamanan Siber & Deteksi Ancaman Malware (DGA Detection Platform)"),
        ("Model ML Utama", "Random Forest Classifier (Akurasi: 87,59%, Presisi: 93,79%, Recall: 80,51%, F1: 86,64%)"),
        ("Mesin Basis Data", "MySQL RDBMS (XAMPP localhost:3306, Database: dga_detection_system) dengan Dual-Engine Fallback SQLite"),
        ("Arsitektur Antarmuka", "Berbasis Web Terpisah: Front-End (SOC Analyst) & Back-End (Administrator)"),
        ("Batas Tanggal Pengumpulan", "14 November 2026, 23:59 WIB (Terselesaikan Lebih Awal)")
    ]
    for i, (k, v) in enumerate(meta_info):
        row = tbl_meta.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.3)
        c2.width = Inches(4.2)
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c1, 70, 70, 110, 110)
        set_cell_margins(c2, 70, 70, 110, 110)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(k)
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.bold = True
        r1.font.color.rgb = c_primary

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(1)
        r2 = p2.add_run(v)
        r2.font.name = "Arial"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = c_text

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ---------------------------------------------------------
    # BAB 1: RINGKASAN EKSEKUTIF & LATAR BELAKANG SISTEM
    # ---------------------------------------------------------
    add_heading_with_spacing(doc, "1. Ringkasan Eksekutif & Latar Belakang Sistem", level=1)

    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.line_spacing = 1.15
    p_desc.paragraph_format.space_after = Pt(8)
    p_desc.add_run(
        "Sistem Deteksi Domain Generation Algorithm (DGA) adalah sebuah platform keamanan siber cerdas "
        "(intelligent cyber security platform) yang dirancang secara khusus untuk mengidentifikasi, menganalisis, "
        "dan memutus jalur komunikasi malware/botnet ke server pengendali Command and Control (C2). Dalam insiden siber modern, "
        "penyerang menggunakan algoritma DGA untuk menghasilkan ratusan hingga ribuan domain pseudo-random setiap hari, "
        "sehingga metode penyaringan daftar hitam statis (static blacklist) tidak lagi efektif. "
        "Sistem ini mengatasi masalah tersebut dengan menerapkan Machine Learning, khususnya "
    )
    r_rf = p_desc.add_run("Random Forest Classifier")
    r_rf.font.bold = True
    p_desc.add_run(
        ", yang mengekstraksi 4 fitur leksikal utama dari nama domain (Domain Length, Vowel Ratio, Digit Ratio, dan Shannon Entropy) "
        "untuk membedakan secara instan antara domain operasional yang sah (Legit) dan domain hasil komputasi algoritma penyerang (DGA)."
    )

    # Gambar 1: Arsitektur Pipeline
    img1_path = os.path.join(ASSETS_DIR, 'gambar_1_arsitektur_pipeline.png')
    if os.path.exists(img1_path):
        doc.add_picture(img1_path, width=Inches(6.4))
        add_caption(doc, "Gambar 1: Diagram Arsitektur & Siklus End-to-End Pipeline Deteksi DGA", c_slate)

    # ---------------------------------------------------------
    # BAB 2: PROGRESS PENGERJAAN BASIS DATA (DATABASE)
    # ---------------------------------------------------------
    add_heading_with_spacing(doc, "2. Progress Pengerjaan: Basis Data (Database)", level=1)

    p_db = doc.add_paragraph()
    p_db.paragraph_format.line_spacing = 1.15
    p_db.paragraph_format.space_after = Pt(8)
    p_db.add_run(
        "Basis data sistem telah selesai dibangun secara menyeluruh menggunakan mesin basis data relasional server "
    )
    r_sql = p_db.add_run("MySQL (XAMPP MariaDB pada port 3306, nama database: dga_detection_system)")
    r_sql.font.bold = True
    p_db.add_run(
        " dengan struktur penyimpanan InnoDB dan relasi kunci tamu (Foreign Key Constraints) lengkap antar tabel, "
        "serta didukung modul adapter dual-engine dengan fallback otomatis ke SQLite (database.db). "
        "Struktur tabel dirancang dengan integritas data tinggi, indeksasi cepat untuk pencarian kueri DNS skala masif "
        "(high-throughput read), pencatatan jejak audit regulasi keamanan (immutable audit trail), penyimpanan metrik evaluasi model, "
        "serta isolasi otomatis domain berbahaya ke DNS Sinkhole (10.10.10.254). Seluruh 8 tabel utama aktif dan terhubung penuh:"
    )

    # Table of DB Tables
    tbl_db = doc.add_table(rows=9, cols=3)
    tbl_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_db.autofit = False

    headers = ["Nama Tabel", "Peran & Fungsi dalam Sistem Keamanan", "Status Pengerjaan"]
    hdr_row = tbl_db.rows[0]
    for idx, text in enumerate(headers):
        cell = hdr_row.cells[idx]
        set_cell_background(cell, "0284C7")
        set_cell_margins(cell, 90, 90, 110, 110)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    db_details = [
        ("users", "Pengelolaan data akun pengguna berbasis peran (Role-Based Access Control) yang memisahkan hak akses Security Analyst dengan Administrator.", "Selesai (100% Aktif)"),
        ("settings", "Penyimpanan konfigurasi global sistem: Decision Threshold (default: 0.42), target IP Sinkhole, webhook alerting channel. Terhubung ke users via updated_by_user_id.", "Selesai (100% Aktif)"),
        ("audit_logs", "Buku besar jejak audit tak terhapus (immutable audit trail) yang mencatat waktu, user, aksi, rincian aktivitas, dan IP address demi kepatuhan ISO 27001. Terhubung ke users via user_id.", "Selesai (100% Aktif)"),
        ("api_keys", "Manajemen otorisasi kunci API 256-bit (X-API-Key) untuk integrasi sensor jaringan eksternal dan aplikasi pihak ketiga. Terhubung ke users via user_id.", "Selesai (100% Aktif)"),
        ("dataset", "Korpus basis pengetahuan latih berisi 1.338 sampel domain berlabel (638 domain sah operasional dan 700 domain malware DGA sintetis/riil). Terhubung ke users via uploaded_by_user_id.", "Selesai (100% Aktif)"),
        ("model_metrics", "Menyimpan riwayat metrik kualitas inferensi Random Forest (Akurasi, Presisi, Recall, F1) serta 4 nilai visual Confusion Matrix (TP, FP, FN, TN). Terhubung ke users via trained_by_user_id.", "Selesai (100% Aktif)"),
        ("dns_logs", "Menyimpan rekaman lalu lintas kueri DNS jaringan beserta stempel waktu, IP sumber, nama domain, 4 fitur leksikal, probabilitas DGA, dan aksi mitigasi. Terhubung ke api_keys via api_key_id.", "Selesai (100% Aktif)"),
        ("blocked_domains", "Menampung daftar hitam (blacklist) domain DGA aktif yang telah diisolasi ke DNS Sinkhole (10.10.10.254) untuk sinkronisasi otomatis ke perimeter firewall. Terhubung ke dns_logs via dns_log_id.", "Selesai (100% Aktif)")
    ]

    col_widths = [Inches(1.5), Inches(3.7), Inches(1.3)]
    for i, (t_name, t_desc, t_stat) in enumerate(db_details):
        row = tbl_db.rows[i+1]
        for col_idx, width in enumerate(col_widths):
            row.cells[col_idx].width = width
            set_cell_margins(row.cells[col_idx], 70, 70, 90, 90)
            if (i % 2 == 1):
                set_cell_background(row.cells[col_idx], "F8FAFC")
            else:
                set_cell_background(row.cells[col_idx], "FFFFFF")

        p0 = row.cells[0].paragraphs[0]
        r0 = p0.add_run(t_name)
        r0.font.name = "Arial"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = c_primary

        p1 = row.cells[1].paragraphs[0]
        r1 = p1.add_run(t_desc)
        r1.font.name = "Arial"
        r1.font.size = Pt(8)
        r1.font.color.rgb = c_text

        p2 = row.cells[2].paragraphs[0]
        r2 = p2.add_run(t_stat)
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(5, 150, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Gambar 2: Screenshot Asli phpMyAdmin Designer (Full HD dari laptop pengguna)
    img_real_hd = os.path.join(ASSETS_DIR, 'gambar_asli_phpmyadmin_user_hd.png')
    img_real_crop = os.path.join(ASSETS_DIR, 'gambar_database_designer_cropped.jpg')
    img_to_use = img_real_hd if os.path.exists(img_real_hd) else img_real_crop

    if os.path.exists(img_to_use):
        doc.add_picture(img_to_use, width=Inches(6.4))
        add_caption(doc, "Gambar 2: Tangkapan Layar Asli Skema Relasi Basis Data MySQL (dga_detection_system) pada Menu Designer phpMyAdmin XAMPP (Localhost Pengembang)", c_slate)

    # Gambar 3: ERD Diagram
    img2_path = os.path.join(ASSETS_DIR, 'gambar_2_erd_database.png')
    if os.path.exists(img2_path):
        doc.add_picture(img2_path, width=Inches(6.4))
        add_caption(doc, "Gambar 3: Entity Relationship Diagram (ERD) Konseptual Basis Data Relasional Sistem Deteksi DGA", c_slate)

    # ---------------------------------------------------------
    # BAB 3: PROGRESS PENGERJAAN TAMPILAN ANTARMUKA (INTERFACE)
    # ---------------------------------------------------------
    add_heading_with_spacing(doc, "3. Progress Pengerjaan: Tampilan Antarmuka (Interface)", level=1)

    p_ui = doc.add_paragraph()
    p_ui.paragraph_format.line_spacing = 1.15
    p_ui.paragraph_format.space_after = Pt(8)
    p_ui.add_run(
        "Antarmuka sistem telah selesai dibangun secara menyeluruh menggunakan prinsip desain modern "
    )
    r_br = p_ui.add_run("Bright & Clean Modern Light Theme")
    r_br.font.bold = True
    p_ui.add_run(
        ". Seluruh tangkapan layar di bawah ini diambil secara langsung (live browser capture) dari aplikasi web aktif "
        "yang berjalan pada server lokal (http://127.0.0.1:5000). Antarmuka menggunakan palet warna terang yang ramah mata "
        "(Eye-Comfort Light Palette) berlatar belakang putih bersih dan abu-abu lembut (#f8fafc), dipadukan dengan tipografi "
        "profesional (Inter & JetBrains Mono), serta aksen warna pastel untuk kartu metrik analitik. "
        "Hak akses dan tata letak menu dipisahkan secara tegas antara "
    )
    r_fe = p_ui.add_run("Front-End (Security Analyst)")
    r_fe.font.bold = True
    p_ui.add_run(" dan ")
    r_be = p_ui.add_run("Back-End (Administrator)")
    r_be.font.bold = True
    p_ui.add_run(":")

    # Subsection A: Front-End
    add_heading_with_spacing(doc, "A. Antarmuka Pengguna Front-End (Security Analyst - SOC)", level=2, before=10, after=4)

    fe_points = [
        ("Dashboard Utama (Executive Overview):", " Menampilkan 4 kartu ringkasan metrik harian (Total DNS Queries: 54, Ancaman DGA: 28, Kueri Sah: 26, dan Status Tingkat Bahaya Jaringan: CRITICAL), grafik visual tren lalu lintas kueri DNS per jam menggunakan Chart.js, diagram rasio domain sah vs DGA, serta tabel peringatan dini ancaman C2 terkini."),
        ("Single Domain Scanner (Pemindai Mandiri):", " Alat investigasi cepat bagi analis SOC untuk menguji nama domain mencurigakan (FQDN). Sistem mengekstraksi 4 fitur leksikal secara transparan (Domain Length, Vowel Ratio, Digit Ratio, Shannon Entropy), menghasilkan hasil klasifikasi (DGA Threat / Legit), skor keyakinan model (Confidence Score), serta rekomendasi tindakan mitigasi."),
        ("Real-Time DNS Log Stream (Live Feed):", " Tabel pemantauan interaktif yang menampilkan aliran kueri DNS jaringan secara langsung (live stream) mencakup stempel waktu milidetik, IP sumber lalu lintas, nama domain, skor entropi Shannon, probabilitas DGA, dan status tindakan mitigasi (Allow/Sinkhole). Dilengkapi tombol 'Simulasikan Traffic Masuk' untuk menguji respon seketika (sub-millisecond latency).")
    ]
    for title, desc in fe_points:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.line_spacing = 1.15
        p_p.paragraph_format.space_before = Pt(2)
        p_p.paragraph_format.space_after = Pt(3)
        r_t = p_p.add_run("• " + title)
        r_t.font.bold = True
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = c_primary
        r_d = p_p.add_run(desc)
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = c_text

    # Gambar 4: Real Web Dashboard
    img_dash = os.path.join(ASSETS_DIR, 'real_web_dashboard.png')
    if os.path.exists(img_dash):
        doc.add_picture(img_dash, width=Inches(6.4))
        add_caption(doc, "Gambar 4: Tangkapan Layar Asli Antarmuka Front-End: Executive Security Overview & Visualisasi Tren Kueri DNS (http://127.0.0.1:5000/)", c_slate)

    # Gambar 5: Real Web Single Scanner
    img_scan = os.path.join(ASSETS_DIR, 'real_web_scanner.png')
    if os.path.exists(img_scan):
        doc.add_picture(img_scan, width=Inches(6.4))
        add_caption(doc, "Gambar 5: Tangkapan Layar Asli Antarmuka Front-End: Pemindai Domain Mandiri / Instant Scanner (http://127.0.0.1:5000/analyst/scanner)", c_slate)

    # Gambar 6: Real Web DNS Stream
    img_stream = os.path.join(ASSETS_DIR, 'real_web_dns_stream.png')
    if os.path.exists(img_stream):
        doc.add_picture(img_stream, width=Inches(6.4))
        add_caption(doc, "Gambar 6: Tangkapan Layar Asli Antarmuka Front-End: Real-Time DNS Log Stream & Simulasi Traffic (http://127.0.0.1:5000/analyst/stream)", c_slate)

    # Subsection B: Back-End
    add_heading_with_spacing(doc, "B. Antarmuka Administrator Back-End (System & Security Admin)", level=2, before=10, after=4)

    be_points = [
        ("Model Management & Evaluation Metrics:", " Dasbor evaluasi kualitas algoritma aktif yang menampilkan 4 metrik performa utama: Akurasi (87,59%), Presisi (93,79%), Recall (80,51%), dan F1-Score (86,64%). Dilengkapi visualisasi Confusion Matrix 2x2 (TP: 665, FP: 44, FN: 161, TN: 782) serta grafik Feature Importance leksikal."),
        ("Decision Threshold Tuning:", " Slider interaktif (0.10 hingga 0.90) yang memungkinkan administrator menggeser ambang batas klasifikasi (dari default 0,50 ke rentang optimal 0,40–0,42) untuk meningkatkan sensitivitas deteksi (Recall) terhadap varian DGA agresif tanpa perlu memprogram ulang model."),
        ("Firewall & DNS Sinkhole Integration:", " Modul sinkronisasi yang mengubah temuan DGA menjadi format aturan jaringan perimeter. Menampilkan daftar domain terisolasi ke DNS Sinkhole (10.10.10.254), serta tombol ekspor aturan ke format Linux iptables dan Cisco/BIND9 Response Policy Zone (RPZ)."),
        ("Dataset Management & Retraining Pipeline:", " Statistik korpus latihan (1.338 sampel domain), fasilitas upload dataset CSV/Excel baru, dan tombol retraining model otomatis yang mengekstraksi ulang fitur leksikal dan memperbarui model Random Forest secara langsung di server."),
        ("API & Webhook Management:", " Panel pembuatan token otorisasi API Key 256-bit (X-API-Key) untuk integrasi dengan sensor jaringan eksternal, serta formulir konfigurasi Webhook ke Discord atau Telegram Bot untuk notifikasi seketika saat terdeteksi ancaman kritis."),
        ("System Health & Infrastructure Monitoring:", " Pemantauan status utilisasi CPU (%), pemakaian memori RAM, kapasitas disk server, dan pengukuran waktu latensi rata-rata prediksi model (inference latency dalam milidetik)."),
        ("User Access Control & Immutable Audit Trail:", " Manajemen pengguna berbasis peran (RBAC) dan buku besar audit trail yang merekam seluruh aktivitas konfigurasi demi kepatuhan regulasi keamanan.")
    ]
    for title, desc in be_points:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.line_spacing = 1.15
        p_p.paragraph_format.space_before = Pt(2)
        p_p.paragraph_format.space_after = Pt(3)
        r_t = p_p.add_run("• " + title)
        r_t.font.bold = True
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = c_primary
        r_d = p_p.add_run(desc)
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = c_text

    # Gambar 7: Real Web Model Management
    img_model = os.path.join(ASSETS_DIR, 'real_web_admin_model.png')
    if os.path.exists(img_model):
        doc.add_picture(img_model, width=Inches(6.4))
        add_caption(doc, "Gambar 7: Tangkapan Layar Asli Antarmuka Back-End: Model Management, Confusion Matrix & Metrik Evaluasi (http://127.0.0.1:5000/admin/model)", c_slate)

    # Gambar 8: Real Web Decision Threshold Slider
    img_thresh = os.path.join(ASSETS_DIR, 'real_web_admin_threshold.png')
    if os.path.exists(img_thresh):
        doc.add_picture(img_thresh, width=Inches(6.4))
        add_caption(doc, "Gambar 8: Tangkapan Layar Asli Antarmuka Back-End: Decision Threshold Tuning Slider (http://127.0.0.1:5000/admin/threshold)", c_slate)

    # Gambar 9: Real Web Firewall & Sinkhole
    img_fw = os.path.join(ASSETS_DIR, 'real_web_admin_firewall.png')
    if os.path.exists(img_fw):
        doc.add_picture(img_fw, width=Inches(6.4))
        add_caption(doc, "Gambar 9: Tangkapan Layar Asli Antarmuka Back-End: Firewall & DNS Sinkhole Integration (http://127.0.0.1:5000/admin/firewall)", c_slate)

    # Gambar 10: Real Web Dataset Management
    img_data = os.path.join(ASSETS_DIR, 'real_web_admin_dataset.png')
    if os.path.exists(img_data):
        doc.add_picture(img_data, width=Inches(6.4))
        add_caption(doc, "Gambar 10: Tangkapan Layar Asli Antarmuka Back-End: Dataset Management & Retraining Pipeline (http://127.0.0.1:5000/admin/dataset)", c_slate)

    # Gambar 11: Real Web System Health
    img_health = os.path.join(ASSETS_DIR, 'real_web_admin_health.png')
    if os.path.exists(img_health):
        doc.add_picture(img_health, width=Inches(6.4))
        add_caption(doc, "Gambar 11: Tangkapan Layar Asli Antarmuka Back-End: System Health & Infrastructure Monitoring (http://127.0.0.1:5000/admin/health)", c_slate)

    # Gambar 12: Real Web User Control & Audit Trail
    img_audit = os.path.join(ASSETS_DIR, 'real_web_admin_audit.png')
    if os.path.exists(img_audit):
        doc.add_picture(img_audit, width=Inches(6.4))
        add_caption(doc, "Gambar 12: Tangkapan Layar Asli Antarmuka Back-End: User Access Control & Immutable Audit Trail (http://127.0.0.1:5000/admin/users)", c_slate)

    # ---------------------------------------------------------
    # BAB 4: RENCANA KERJA: YANG BELUM DAN AKAN DIKERJAKAN (ROADMAP)
    # ---------------------------------------------------------
    add_heading_with_spacing(doc, "4. Rencana Kerja: Yang Belum dan Akan Dikerjakan (Roadmap)", level=1)

    p_road_intro = doc.add_paragraph()
    p_road_intro.paragraph_format.line_spacing = 1.15
    p_road_intro.paragraph_format.space_after = Pt(6)
    p_road_intro.add_run(
        "Meskipun seluruh fungsionalitas inti, basis data MySQL, pipeline machine learning, dan antarmuka web "
        "telah beroperasi secara penuh dan siap didemonstrasikan, berikut adalah rencana pengembangan strategis "
        "tahap lanjutan (roadmap) yang dirancang untuk memperkuat kemampuan operasional sistem menuju skala enterprise:"
    )

    roadmap_items = [
        ("1. Implementasi Live Packet Capture Perangkat Keras Jaringan (Network TAP / SPAN Port):",
         "Saat ini kueri DNS disimulasikan dan dipasok melalui API/log feeder. Tahap selanjutnya yang akan dikerjakan adalah memasang modul penyadap paket mentah langsung pada interface kartu jaringan (NIC Promiscuous Mode via Scapy / WinPcap / AF_PACKET) untuk membedah paket DNS Port 53 UDP/TCP secara non-intrusif langsung dari switch core jaringan."),

        ("2. Peningkatan Algoritma Deep Learning untuk DGA Berbasis Kamus (Dictionary-based DGA):",
         "Model Random Forest saat ini sangat unggul pada DGA berbasis entropi tinggi (seperti Conficker dan Cryptolocker). Namun, untuk menangkal varian botnet modern yang menggabungkan kata-kata kamus bahasa alami (seperti Suppobox dan Matsnu) yang memiliki entropi mirip domain sah, akan dikembangkan model Deep Learning pendamping (Bi-LSTM atau Transformer / DistilBERT)."),

        ("3. Otomatisasi Orkestrasi Pemblokiran ke Perangkat Firewall Fisik (Live SDN/Firewall API):",
         "Saat ini sistem mengekspor aturan format IPTables dan RPZ. Tahap yang akan dikerjakan adalah membangun konektor aktif menggunakan API RESTCONF / NETCONF ke router MikroTik RouterOS, pfSense XML-RPC, Palo Alto Networks, dan Cloudflare Gateway agar saat domain DGA terdeteksi, isolasi rute terjadi seketika di level hardware."),

        ("4. Distribusi Threat Intelligence Terstandar (Format OASIS STIX 2.1 & TAXII):",
         "Fitur pertukaran informasi ancaman terstandar industri agar temuan domain DGA dari sistem ini dapat diekspor dan dibagikan secara otomatis ke ekosistem SIEM nasional (seperti BSSN CSIRT / Gov-CSIRT) untuk perlindungan infrastruktur informasi vital."),

        ("5. Penguatan Keamanan Akses: Autentikasi Dua Faktor (MFA) & Integrasi LDAP/SSO:",
         "Peningkatan sistem RBAC saat ini dengan menambahkan otentikasi multi-faktor (MFA berbasis TOTP Google Authenticator) serta integrasi Single Sign-On (SSO) berbasis protokol SAML 2.0 / OpenID Connect dengan Active Directory enterprise."),

        ("6. Pengujian Beban Ekstrem & Caching Kinerja Tinggi (> 10.000 QPS):",
         "Melakukan stress testing dan load testing simulasi beban tinggi (high-throughput DNS query) menggunakan DNSperf serta menambahkan lapisan caching whitelisting berbasis in-memory Redis / Bloom Filter untuk menjamin latensi inferensi tetap di bawah 1 milidetik saat melayani jutaan kueri harian.")
    ]

    for r_title, r_desc in roadmap_items:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.line_spacing = 1.15
        p_r.paragraph_format.space_before = Pt(3)
        p_r.paragraph_format.space_after = Pt(3)
        r_t = p_r.add_run(r_title + "\n")
        r_t.font.bold = True
        r_t.font.size = Pt(9)
        r_t.font.color.rgb = c_primary
        r_d = p_r.add_run(r_desc)
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = c_text

    # ---------------------------------------------------------
    # BAB 5: KESIMPULAN & TAUTAN REPOSITORI
    # ---------------------------------------------------------
    add_heading_with_spacing(doc, "5. Kesimpulan & Tautan Repositori Proyek", level=1)

    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.paragraph_format.space_after = Pt(8)
    p_conc.add_run(
        "Seluruh capaian pengerjaan sistem deteksi DGA berbasis machine learning telah memenuhi target fungsional "
        "yang ditetapkan, mencakup integritas basis data relasional 8 tabel di MySQL XAMPP, akurasi model Random Forest yang teruji "
        "(Akurasi: 87,59%, Presisi: 93,79%, Recall: 80,51%, F1: 86,64%), serta penyajian antarmuka web modern bertema terang "
        "yang memisahkan peran Analis SOC dan Administrator. Seluruh kode sumber, model, basis data, dan template "
        "telah dikelola secara terstruktur dan diunggah ke repositori GitHub resmi:"
    )

    # Callout Box for GitHub
    tbl_gh = doc.add_table(rows=1, cols=1)
    tbl_gh.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_gh = tbl_gh.rows[0].cells[0]
    c_gh.width = Inches(6.5)
    set_cell_background(c_gh, "F0F9FF")
    set_cell_margins(c_gh, 80, 80, 130, 130)
    p_gh = c_gh.paragraphs[0]
    p_gh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gh1 = p_gh.add_run("Tautan Repositori GitHub Resmi Proyek:\n")
    r_gh1.font.bold = True
    r_gh1.font.size = Pt(9.5)
    r_gh1.font.color.rgb = c_blue
    r_gh2 = p_gh.add_run("https://github.com/aidilsy06-cloud/dga-detection-system")
    r_gh2.font.bold = True
    r_gh2.font.size = Pt(10.5)
    r_gh2.font.color.rgb = c_dark_blue

    # Save to primary DOCX
    doc.save(DOCX_OUT)
    print(f"[+] Successfully generated DOCX report: {DOCX_OUT}")

    # Also save to extra copy in workspace
    doc.save(DOCX_OUT_EXTRA)
    print(f"[+] Successfully generated extra DOCX report: {DOCX_OUT_EXTRA}")

if __name__ == '__main__':
    create_report()
