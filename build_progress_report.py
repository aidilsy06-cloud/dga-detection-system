import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'doc_assets')
DOCX_OUT = os.path.join(BASE_DIR, 'Laporan_Progress_Sistem_Deteksi_DGA.docx')

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Set Margins (2.54 cm / 1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Colors
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
    run_badge = p_badge.add_run("LAPORAN PROGRESS TUGAS PROYEK REKAYASA SISTEM")
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
    p_sub.paragraph_format.space_after = Pt(18)
    run_sub = p_sub.add_run("Platform Keamanan Siber Cerdas untuk Deteksi & Mitigasi Jalur Komunikasi Malware Command and Control (C2)")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(10.5)
    run_sub.font.color.rgb = c_slate

    # Meta Table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False

    meta_info = [
        ("Topik Proyek", "Sistem Keamanan Siber & Deteksi Ancaman Malware (DGA Detection)"),
        ("Model ML Utama", "Random Forest Classifier (Akurasi: 87,59%, Presisi: 93,79%, Recall: 80,51%, F1: 86,64%)"),
        ("Arsitektur Sistem", "Berbasis Web Terpisah: Front-End (SOC Analyst) & Back-End (Administrator)"),
        ("Batas Tanggal Pengumpulan", "14 November 2026, 23:59 WIB")
    ]
    for i, (k, v) in enumerate(meta_info):
        row = tbl_meta.rows[i]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c1, 80, 80, 120, 120)
        set_cell_margins(c2, 80, 80, 120, 120)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(k)
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = c_primary

        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(v)
        r2.font.name = "Arial"
        r2.font.size = Pt(9)
        r2.font.color.rgb = c_text

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ---------------------------------------------------------
    # RINGKASAN EKSEKUTIF
    # ---------------------------------------------------------
    h1 = doc.add_heading("1. Ringkasan Eksekutif & Latar Belakang Sistem", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

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

    # Insert Architecture Diagram
    img1_path = os.path.join(ASSETS_DIR, 'gambar_1_arsitektur_pipeline.png')
    if os.path.exists(img1_path):
        doc.add_picture(img1_path, width=Inches(6.4))
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(14)
        r_c1 = p_cap1.add_run("Gambar 1: Diagram Arsitektur & Siklus End-to-End Pipeline Deteksi DGA")
        r_c1.font.name = "Arial"
        r_c1.font.size = Pt(8.5)
        r_c1.font.italic = True
        r_c1.font.color.rgb = c_slate

    # ---------------------------------------------------------
    # BAB I: PROGRESS DATABASE
    # ---------------------------------------------------------
    h2 = doc.add_heading("2. Progress Pengerjaan: Basis Data (Database)", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    p_db = doc.add_paragraph()
    p_db.paragraph_format.line_spacing = 1.15
    p_db.paragraph_format.space_after = Pt(8)
    p_db.add_run(
        "Basis data sistem telah selesai dibangun secara menyeluruh menggunakan mesin basis data relasional "
    )
    r_sql = p_db.add_run("SQLite 3 (database.db)")
    r_sql.font.bold = True
    p_db.add_run(
        ". Struktur tabel dirancang dengan integritas data tinggi untuk mendukung operasi pembacaan kueri cepat "
        "(high-throughput read), pencatatan jejak audit regulasi keamanan (immutable audit trail), penyimpanan metrik evaluasi model, "
        "serta isolasi otomatis domain berbahaya ke DNS Sinkhole. Terdapat 8 tabel utama yang telah aktif dan terisi data operasional:"
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
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    db_details = [
        ("dns_logs", "Menyimpan seluruh rekaman lalu lintas kueri DNS jaringan beserta stempel waktu, IP sumber, nama domain, 4 fitur leksikal, probabilitas DGA, dan aksi mitigasi.", "Selesai (100% Aktif)"),
        ("blocked_domains", "Menampung daftar hitam (blacklist) domain DGA aktif yang telah diisolasi ke DNS Sinkhole (10.10.10.254) untuk sinkronisasi otomatis ke perimeter firewall.", "Selesai (100% Aktif)"),
        ("model_metrics", "Menyimpan riwayat metrik kualitas inferensi Random Forest (Akurasi, Presisi, Recall, F1) serta 4 nilai visual Confusion Matrix (TP, FP, FN, TN).", "Selesai (100% Aktif)"),
        ("settings", "Penyimpanan konfigurasi parameter global sistem: Decision Threshold (default: 0.42), target IP Sinkhole, webhook alerting channel, dan severity filter.", "Selesai (100% Aktif)"),
        ("dataset", "Korpus basis pengetahuan latih berisi 1.338 sampel domain berlabel (638 domain sah operasional dan 700 domain malware DGA sintetis/riil).", "Selesai (100% Aktif)"),
        ("api_keys", "Manajemen otorisasi kunci API 256-bit (X-API-Key) untuk integrasi dengan sensor jaringan eksternal dan aplikasi pihak ketiga.", "Selesai (100% Aktif)"),
        ("users", "Pengelolaan data akun pengguna berbasis peran (Role-Based Access Control) yang memisahkan hak akses Security Analyst dengan Administrator.", "Selesai (100% Aktif)"),
        ("audit_logs", "Buku besar jejak audit tak terhapus (immutable audit trail) yang mencatat waktu, user, aksi, rincian aktivitas, dan IP address demi kepatuhan ISO 27001.", "Selesai (100% Aktif)")
    ]

    col_widths = [Inches(1.5), Inches(3.7), Inches(1.3)]
    for i, (t_name, t_desc, t_stat) in enumerate(db_details):
        row = tbl_db.rows[i+1]
        for col_idx, width in enumerate(col_widths):
            row.cells[col_idx].width = width
            set_cell_margins(row.cells[col_idx], 80, 80, 100, 100)
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
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = c_text

        p2 = row.cells[2].paragraphs[0]
        r2 = p2.add_run(t_stat)
        r2.font.name = "Arial"
        r2.font.size = Pt(8)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(5, 150, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Insert ERD Diagram
    img2_path = os.path.join(ASSETS_DIR, 'gambar_2_erd_database.png')
    if os.path.exists(img2_path):
        doc.add_picture(img2_path, width=Inches(6.4))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(14)
        r_c2 = p_cap2.add_run("Gambar 2: Entity Relationship Diagram (ERD) Basis Data Relasional Sistem")
        r_c2.font.name = "Arial"
        r_c2.font.size = Pt(8.5)
        r_c2.font.italic = True
        r_c2.font.color.rgb = c_slate

    # ---------------------------------------------------------
    # BAB II: PROGRESS TAMPILAN / INTERFACE
    # ---------------------------------------------------------
    h3 = doc.add_heading("3. Progress Pengerjaan: Tampilan Antarmuka (Interface)", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

    p_ui = doc.add_paragraph()
    p_ui.paragraph_format.line_spacing = 1.15
    p_ui.paragraph_format.space_after = Pt(8)
    p_ui.add_run(
        "Antarmuka sistem telah selesai dibangun secara menyeluruh menggunakan prinsip desain modern "
    )
    r_br = p_ui.add_run("Bright & Clean Modern Light Theme")
    r_br.font.bold = True
    p_ui.add_run(
        " berbasis Bootstrap 5, Chart.js, Google Fonts Inter, dan JetBrains Mono. "
        "Sistem menerapkan pemisahan peran yang tegas (*Role-Based Access Control*) dengan fitur tombol "
    )
    r_sw = p_ui.add_run("Role Switcher")
    r_sw.font.bold = True
    p_ui.add_run(
        " di bilah navigasi atas yang memungkinkan penguji berganti peran seketika antara Front-End (Analis SOC) "
        "dan Back-End (Administrator Sistem):"
    )

    # Sub-Heading: Front-End
    h3_fe = doc.add_heading("A. Antarmuka Pengguna Front-End (Security Analyst - SOC)", level=2)
    h3_fe.paragraph_format.space_before = Pt(10)
    h3_fe.paragraph_format.space_after = Pt(4)

    fe_bullets = [
        ("Dashboard Utama (Executive Overview):", "Menampilkan 4 kartu ringkasan metrik harian (Total DNS Queries, Ancaman DGA Terdeteksi, Kueri Sah, Tingkat Ancaman Jaringan), grafik visual interaktif tren lalu lintas DNS 24 jam dengan Chart.js, diagram donat rasio ancaman, dan tabel investigasi insiden terkini."),
        ("Single Domain Scanner (Pemindai Mandiri):", "Alat uji instan satu nama domain (FQDN). Sistem seketika mengekstraksi 4 fitur leksikal dalam format kartu pastel (Panjang Domain, Rasio Vokal, Rasio Angka, Entropi Shannon), menghitung probabilitas AI, menampilkan tingkat keyakinan (confidence score), serta status mitigasi otomatis ke Sinkhole."),
        ("Batch Upload Inspection (Inspeksi Log Massal):", "Fasilitas inspeksi file log jaringan (CSV, TXT, LOG, Excel) secara massal. Dilengkapi kartu statistik ringkasan, tabel dinamis dengan penyaring instan (Semua / Hanya DGA / Hanya Legit), pencarian nama domain, serta fitur ekspor CSV dan unduh Laporan Investigasi Resmi Format PDF siap cetak."),
        ("Real-Time DNS Log Stream:", "Tabel pemantauan interaktif yang menampilkan aliran kueri DNS jaringan secara kronologis (live feed). Menyediakan stempel waktu, IP sumber klien, nama domain, skor entropi, probabilitas DGA, dan status tindakan (Allowed/Sinkhole), dilengkapi tombol Pause/Resume, pembersih layar, dan tombol Simulasi Traffic Masuk.")
    ]
    for b_title, b_desc in fe_bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15
        bp.paragraph_format.space_after = Pt(4)
        r_bt = bp.add_run(b_title + " ")
        r_bt.font.bold = True
        r_bt.font.color.rgb = c_primary
        r_bd = bp.add_run(b_desc)
        r_bd.font.color.rgb = c_text

    # Insert FE Mockup 1 (Dashboard & Scanner)
    img3_path = os.path.join(ASSETS_DIR, 'gambar_3_frontend_dashboard_scanner.png')
    if os.path.exists(img3_path):
        doc.add_picture(img3_path, width=Inches(6.4))
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap3.paragraph_format.space_after = Pt(10)
        r_c3 = p_cap3.add_run("Gambar 3: Tampilan Antarmuka Front-End: Executive Dashboard & Single Domain Scanner")
        r_c3.font.name = "Arial"
        r_c3.font.size = Pt(8.5)
        r_c3.font.italic = True
        r_c3.font.color.rgb = c_slate

    # Insert FE Mockup 2 (Batch & Stream)
    img4_path = os.path.join(ASSETS_DIR, 'gambar_4_frontend_batch_stream.png')
    if os.path.exists(img4_path):
        doc.add_picture(img4_path, width=Inches(6.4))
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.paragraph_format.space_after = Pt(14)
        r_c4 = p_cap4.add_run("Gambar 4: Tampilan Antarmuka Front-End: Batch Upload Inspection & Real-Time DNS Stream")
        r_c4.font.name = "Arial"
        r_c4.font.size = Pt(8.5)
        r_c4.font.italic = True
        r_c4.font.color.rgb = c_slate

    # Sub-Heading: Back-End
    h3_be = doc.add_heading("B. Antarmuka Administrator Back-End (System & Security Admin)", level=2)
    h3_be.paragraph_format.space_before = Pt(12)
    h3_be.paragraph_format.space_after = Pt(4)

    be_bullets = [
        ("Model Management & Evaluation Metrics:", "Dasbor evaluasi kualitas algoritma aktif yang menampilkan metrik akurasi tinggi: Akurasi 87,59%, Presisi 93,79%, Recall 80,51%, F1-Score 86,64%, visualisasi 2x2 Confusion Matrix (TP: 665, FP: 44, FN: 161, TN: 782), serta diagram Gini Feature Importance."),
        ("Decision Threshold Tuning:", "Slider interaktif (0.10 hingga 0.90) yang memungkinkan administrator menggeser ambang batas klasifikasi (optimal: 0.40 - 0.42) secara seketika guna menyesuaikan sensitivitas deteksi (Recall) tanpa perlu melatih ulang model."),
        ("Firewall & DNS Sinkhole Integration:", "Modul sinkronisasi yang mengubah temuan DGA menjadi aturan pemblokiran jaringan dengan target DNS Sinkhole 10.10.10.254, serta fitur unduh format IPTables (.sh), BIND9 RPZ (.zone), OS Hosts, dan pfSense/Fortinet."),
        ("Dataset Management & Retraining Pipeline:", "Statistik korpus latihan (1.338 sampel), fasilitas unggah dataset tambahan (.csv/.xlsx), dan tombol picu siklus retraining Random Forest terotomasi."),
        ("API & Webhook Management:", "Panel pembuatan token otorisasi API Key 256-bit (X-API-Key), endpoint RESTful POST /api/v1/detect, dan manajemen Webhook Alert ke Discord/Telegram tim SOC."),
        ("System Health & Infrastructure Monitoring:", "Pemantauan status utilisasi CPU (%), RAM (GB), kapasitas Disk (GB), latensi inferensi AI (~1.2 ms), dan status modul engine."),
        ("User Access Control & Immutable Audit Trail:", "Manajemen pengguna berbasis peran (RBAC) dan buku besar audit trail yang merekam seluruh aktivitas konfigurasi demi kepatuhan regulasi keamanan.")
    ]
    for b_title, b_desc in be_bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.line_spacing = 1.15
        bp.paragraph_format.space_after = Pt(4)
        r_bt = bp.add_run(b_title + " ")
        r_bt.font.bold = True
        r_bt.font.color.rgb = c_dark_blue
        r_bd = bp.add_run(b_desc)
        r_bd.font.color.rgb = c_text

    # Insert BE Mockup 1 (Model & Threshold)
    img5_path = os.path.join(ASSETS_DIR, 'gambar_5_admin_model_threshold.png')
    if os.path.exists(img5_path):
        doc.add_picture(img5_path, width=Inches(6.4))
        p_cap5 = doc.add_paragraph()
        p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap5.paragraph_format.space_after = Pt(10)
        r_c5 = p_cap5.add_run("Gambar 5: Tampilan Antarmuka Back-End: Model Management Confusion Matrix & Threshold Tuning")
        r_c5.font.name = "Arial"
        r_c5.font.size = Pt(8.5)
        r_c5.font.italic = True
        r_c5.font.color.rgb = c_slate

    # Insert BE Mockup 2 (Firewall & Dataset)
    img6_path = os.path.join(ASSETS_DIR, 'gambar_6_admin_firewall_dataset.png')
    if os.path.exists(img6_path):
        doc.add_picture(img6_path, width=Inches(6.4))
        p_cap6 = doc.add_paragraph()
        p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap6.paragraph_format.space_after = Pt(10)
        r_c6 = p_cap6.add_run("Gambar 6: Tampilan Antarmuka Back-End: Firewall Sinkhole Integration & Dataset Pipeline")
        r_c6.font.name = "Arial"
        r_c6.font.size = Pt(8.5)
        r_c6.font.italic = True
        r_c6.font.color.rgb = c_slate

    # Insert BE Mockup 3 (API, Health, Audit)
    img7_path = os.path.join(ASSETS_DIR, 'gambar_7_admin_api_health_audit.png')
    if os.path.exists(img7_path):
        doc.add_picture(img7_path, width=Inches(6.4))
        p_cap7 = doc.add_paragraph()
        p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap7.paragraph_format.space_after = Pt(14)
        r_c7 = p_cap7.add_run("Gambar 7: Tampilan Antarmuka Back-End: API/Webhook Dispatcher, Health Monitor, & Audit Trail")
        r_c7.font.name = "Arial"
        r_c7.font.size = Pt(8.5)
        r_c7.font.italic = True
        r_c7.font.color.rgb = c_slate

    # ---------------------------------------------------------
    # BAB III: YANG BELUM DAN AKAN DIKERJAKAN
    # ---------------------------------------------------------
    h4 = doc.add_heading("4. Rencana Kerja: Yang Belum dan Akan Dikerjakan (Roadmap)", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    p_todo = doc.add_paragraph()
    p_todo.paragraph_format.line_spacing = 1.15
    p_todo.paragraph_format.space_after = Pt(8)
    p_todo.add_run(
        "Meskipun seluruh fungsionalitas inti, basis data, pipeline machine learning, dan antarmuka web telah berhasil "
        "beroperasi dengan sangat baik pada tahap prototipe, terdapat sejumlah penyempurnaan skala enterprise "
        "dan fitur tingkat lanjut yang "
    )
    r_todo = p_todo.add_run("belum sepenuhnya diintegrasikan ke lingkungan perangkat keras fisik produksi")
    r_todo.font.bold = True
    p_todo.add_run(
        " dan akan dikerjakan pada siklus pengembangan berikutnya sesuai studi kasus:"
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
        p_r.paragraph_format.space_before = Pt(4)
        p_r.paragraph_format.space_after = Pt(4)
        r_t = p_r.add_run(r_title + "\n")
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = c_primary
        r_d = p_r.add_run(r_desc)
        r_d.font.size = Pt(9)
        r_d.font.color.rgb = c_text

    # ---------------------------------------------------------
    # BAB IV: KESIMPULAN & TAUTAN REPOSITORI
    # ---------------------------------------------------------
    h5 = doc.add_heading("5. Kesimpulan & Tautan Repositori Proyek", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)

    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.paragraph_format.space_after = Pt(8)
    p_conc.add_run(
        "Seluruh capaian pengerjaan sistem deteksi DGA berbasis machine learning telah memenuhi target fungsional "
        "yang ditetapkan, mencakup integritas basis data relasional 8 tabel, akurasi model Random Forest yang teruji "
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
    set_cell_margins(c_gh, 100, 100, 150, 150)
    p_gh = c_gh.paragraphs[0]
    p_gh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gh1 = p_gh.add_run("Tautan Repositori GitHub Resmi:\n")
    r_gh1.font.bold = True
    r_gh1.font.size = Pt(10)
    r_gh1.font.color.rgb = c_blue
    r_gh2 = p_gh.add_run("https://github.com/aidilsy06-cloud/dga-detection-system")
    r_gh2.font.bold = True
    r_gh2.font.size = Pt(11)
    r_gh2.font.color.rgb = c_dark_blue

    doc.save(DOCX_OUT)
    print(f"[+] Successfully generated DOCX report: {DOCX_OUT}")

if __name__ == '__main__':
    create_report()
