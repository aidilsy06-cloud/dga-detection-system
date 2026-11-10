import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'doc_assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

# Set global matplotlib font & styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# 1. Diagram Arsitektur & Pipeline Deteksi DGA
# -------------------------------------------------------------
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=200)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, 'ARSITEKTUR & PIPELINE SISTEM DETEKSI DGA BERBASIS MACHINE LEARNING', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    ax.text(50, 91, 'End-to-End Pipeline: Ingestion -> Feature Engineering -> Random Forest -> Mitigation',
            ha='center', va='center', fontsize=10, color='#64748b')

    # Stage 1: Ingestion
    ax.add_patch(patches.FancyBboxPatch((4, 52), 20, 32, boxstyle="round,pad=1", ec="#0284c7", fc="#f0f9ff", lw=2))
    ax.text(14, 80, '1. DATA INGESTION', ha='center', va='center', fontsize=11, fontweight='bold', color='#0284c7')
    ax.text(14, 73, '• Real-Time DNS Stream\n• Batch Log File Upload\n  (CSV, TXT, PCAP Log)\n• RESTful Ingest API\n• Capture Port 53 UDP',
            ha='center', va='center', fontsize=8.5, color='#334155')

    # Arrow 1->2
    ax.annotate('', xy=(27, 68), xytext=(24, 68), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=3))

    # Stage 2: Feature Engineering
    ax.add_patch(patches.FancyBboxPatch((28, 52), 22, 32, boxstyle="round,pad=1", ec="#7c3aed", fc="#f5f3ff", lw=2))
    ax.text(39, 80, '2. FITUR LEKSIKAL', ha='center', va='center', fontsize=11, fontweight='bold', color='#7c3aed')
    ax.text(39, 72, '• Domain Length\n• Vowel Ratio (a,e,i,o,u)\n• Digit Ratio (0-9)\n• Shannon Entropy (H)\n• StandardScaler Norm',
            ha='center', va='center', fontsize=8.5, color='#334155')

    # Arrow 2->3
    ax.annotate('', xy=(53, 68), xytext=(50, 68), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=3))

    # Stage 3: ML Inference
    ax.add_patch(patches.FancyBboxPatch((54, 52), 21, 32, boxstyle="round,pad=1", ec="#d97706", fc="#fffbeb", lw=2))
    ax.text(64.5, 80, '3. RANDOM FOREST', ha='center', va='center', fontsize=11, fontweight='bold', color='#d97706')
    ax.text(64.5, 72, '• 100 Decision Trees\n• Max Depth: 12\n• Decision Threshold:\n  Optimal: 0.40 - 0.42\n• P(DGA) >= Threshold',
            ha='center', va='center', fontsize=8.5, color='#334155')

    # Arrow 3->4
    ax.annotate('', xy=(78, 68), xytext=(75, 68), arrowprops=dict(arrowstyle="->", color="#d97706", lw=3))

    # Stage 4: Actions & Mitigations
    ax.add_patch(patches.FancyBboxPatch((79, 52), 18, 32, boxstyle="round,pad=1", ec="#dc2626", fc="#fef2f2", lw=2))
    ax.text(88, 80, '4. MITIGASI & AKSI', ha='center', va='center', fontsize=11, fontweight='bold', color='#dc2626')
    ax.text(88, 72, '• DNS Sinkhole (10.10.10.254)\n• Auto Firewall Drop\n• Immutable Audit Trail\n• Telegram/Discord Alert\n• Laporan PDF Resmi',
            ha='center', va='center', fontsize=8.5, color='#334155')

    # Lower Platform Partition: Front-End vs Back-End
    ax.add_patch(patches.FancyBboxPatch((4, 8), 44, 36, boxstyle="round,pad=1", ec="#bae6fd", fc="#ffffff", lw=1.5))
    ax.text(26, 40, 'FRONT-END (SOC SECURITY ANALYST)', ha='center', va='center', fontsize=11, fontweight='bold', color='#0369a1')
    ax.text(26, 24, '1. Executive Overview Dashboard (Tren 24 Jam & Rasio Ancaman)\n2. Single Domain Scanner (Instant Lexical Inference & Confidence)\n3. Batch Upload Inspection (Filterable Table & PDF Report Export)\n4. Real-Time DNS Log Stream (Live Feed & Attack Simulator)',
            ha='center', va='center', fontsize=8.5, color='#475569')

    ax.add_patch(patches.FancyBboxPatch((52, 8), 45, 36, boxstyle="round,pad=1", ec="#ddd6fe", fc="#ffffff", lw=1.5))
    ax.text(74.5, 40, 'BACK-END (SYSTEM & SECURITY ADMINISTRATOR)', ha='center', va='center', fontsize=11, fontweight='bold', color='#6d28d9')
    ax.text(74.5, 24, '1. Model Management & 2x2 Confusion Matrix Visual Grid\n2. Decision Threshold Tuning Slider (Sensitivitas 0.40 - 0.42)\n3. Firewall & Sinkhole Policy Sync (IPTables, RPZ, pfSense, Hosts)\n4. Dataset Management & Retraining Pipeline (Corpus Upload)\n5. REST API & Webhook Dispatcher | 6. Hardware Health Monitor',
            ha='center', va='center', fontsize=8.5, color='#475569')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_1_arsitektur_pipeline.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

# -------------------------------------------------------------
# 2. Entity Relationship Diagram (ERD) Basis Data
# -------------------------------------------------------------
def create_erd_diagram():
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=200)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, 'ENTITY RELATIONSHIP DIAGRAM (ERD) - BASIS DATA SISTEM DETEKSI DGA', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    ax.text(50, 92, 'Basis Data Relasional SQLite (database.db) - 8 Tabel Utama Sistem Keamanan Siber',
            ha='center', va='center', fontsize=9.5, color='#64748b')

    # Table 1: dns_logs
    ax.add_patch(patches.FancyBboxPatch((3, 48), 26, 38, boxstyle="round,pad=0.5", ec="#0284c7", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((3, 81), 26, 5, fc="#0284c7"))
    ax.text(16, 83.5, 'TABEL: dns_logs', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(4, 63, 'PK id: INTEGER (AUTO)\n   timestamp: TEXT\n   source_ip: TEXT\n   domain: TEXT\n   entropy: REAL\n   length: INTEGER\n   vowel_ratio: REAL\n   digit_ratio: REAL\n   dga_probability: REAL\n   classification: TEXT\n   action_taken: TEXT',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Table 2: blocked_domains
    ax.add_patch(patches.FancyBboxPatch((36, 52), 27, 34, boxstyle="round,pad=0.5", ec="#dc2626", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((36, 81), 27, 5, fc="#dc2626"))
    ax.text(49.5, 83.5, 'TABEL: blocked_domains', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(37, 66, 'PK id: INTEGER (AUTO)\n   domain: TEXT (UNIQUE)\n   detected_at: TEXT\n   threat_type: TEXT\n   confidence: REAL\n   status: TEXT (Active/Whitelist)\n\nRelasi: Sinkronisasi dari\ndns_logs (classification=DGA)',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Table 3: model_metrics
    ax.add_patch(patches.FancyBboxPatch((70, 48), 27, 38, boxstyle="round,pad=0.5", ec="#7c3aed", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((70, 81), 27, 5, fc="#7c3aed"))
    ax.text(83.5, 83.5, 'TABEL: model_metrics', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(71, 63, 'PK id: INTEGER (AUTO)\n   accuracy: REAL (87.59%)\n   precision: REAL (93.79%)\n   recall: REAL (80.51%)\n   f1_score: REAL (86.64%)\n   threshold: REAL (0.42)\n   cm_tp: INTEGER (665)\n   cm_fp: INTEGER (44)\n   cm_fn: INTEGER (161)\n   cm_tn: INTEGER (782)\n   last_trained: TEXT',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Table 4: settings
    ax.add_patch(patches.FancyBboxPatch((3, 6), 20, 34, boxstyle="round,pad=0.5", ec="#d97706", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((3, 35), 20, 5, fc="#d97706"))
    ax.text(13, 37.5, 'TABEL: settings', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(4, 20, 'PK key: TEXT\n   value: TEXT\n\nContoh data:\n• threshold: 0.42\n• sinkhole_ip: 10.10.10.254\n• active_algorithm: RF\n• webhook_url: Discord/TG',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Table 5: dataset
    ax.add_patch(patches.FancyBboxPatch((27, 6), 22, 34, boxstyle="round,pad=0.5", ec="#059669", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((27, 35), 22, 5, fc="#059669"))
    ax.text(38, 37.5, 'TABEL: dataset', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(28, 20, 'PK id: INTEGER (AUTO)\n   domain: TEXT\n   length: INTEGER\n   vowel_ratio: REAL\n   digit_ratio: REAL\n   shannon_entropy: REAL\n   label: INT (1/0)\n   source: TEXT\n(1.338 baris sampel)',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Table 6: api_keys
    ax.add_patch(patches.FancyBboxPatch((53, 6), 20, 34, boxstyle="round,pad=0.5", ec="#2563eb", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((53, 35), 20, 5, fc="#2563eb"))
    ax.text(63, 37.5, 'TABEL: api_keys', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(54, 20, 'PK id: INTEGER (AUTO)\n   key_name: TEXT\n   api_key: TEXT (UNIQUE)\n   created_at: TEXT\n   last_used: TEXT\n   status: TEXT (Active)',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Table 7: audit_logs & users
    ax.add_patch(patches.FancyBboxPatch((76, 6), 21, 34, boxstyle="round,pad=0.5", ec="#475569", fc="#ffffff", lw=1.5))
    ax.add_patch(patches.Rectangle((76, 35), 21, 5, fc="#475569"))
    ax.text(86.5, 37.5, 'TABEL: audit_logs', ha='center', va='center', fontsize=10, fontweight='bold', color='#ffffff')
    ax.text(77, 20, 'PK id: INTEGER (AUTO)\n   timestamp: TEXT\n   user: TEXT (analyst/adm)\n   role: TEXT\n   action: TEXT\n   details: TEXT\n   ip_address: TEXT\n(Immutable Audit Log)',
            ha='left', va='center', fontsize=8, color='#334155', fontfamily='monospace')

    # Connectors / Relations
    ax.annotate('', xy=(36, 68), xytext=(29, 68), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=2, ls='--'))
    ax.annotate('', xy=(38, 40), xytext=(70, 55), arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=2, ls='--'))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_2_erd_database.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

# -------------------------------------------------------------
# 3. Visual Mockup: Front-End Dashboard & Single Scanner
# -------------------------------------------------------------
def create_ui_dashboard_scanner():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)
    fig.patch.set_facecolor('#ffffff')

    # Panel 1: Executive Dashboard Mockup
    ax1.set_facecolor('#f8fafc')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title("1. Tampilan Front-End: Executive Dashboard (Overview)", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # 4 Stat Cards
    cards = [
        ("TOTAL QUERIES", "1.240", "#0284c7", "#f0f9ff", 2, 76),
        ("DGA THREATS", "84", "#dc2626", "#fef2f2", 26, 76),
        ("LEGIT TRAFFIC", "1.156", "#059669", "#ecfdf5", 50, 76),
        ("THREAT LEVEL", "HIGH", "#d97706", "#fffbeb", 74, 76)
    ]
    for lbl, val, col, bg, x, y in cards:
        ax1.add_patch(patches.FancyBboxPatch((x, y), 23, 16, boxstyle="round,pad=0.5", ec=col, fc=bg, lw=1))
        ax1.text(x+11.5, y+11, lbl, ha='center', va='center', fontsize=7, fontweight='bold', color=col)
        ax1.text(x+11.5, y+4.5, val, ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a')

    # Trend Chart Mockup Box
    ax1.add_patch(patches.FancyBboxPatch((2, 22), 95, 48, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff", lw=1))
    ax1.text(6, 65, "Grafik Tren Lalu Lintas DNS & Deteksi Ancaman (24 Jam)", fontsize=8.5, fontweight='bold', color='#0f172a')
    # Mini plot inside
    hrs = np.array([8, 10, 12, 14, 16, 18, 20, 22, 0, 2, 4, 6])
    legit_vals = np.array([45, 62, 85, 90, 78, 95, 110, 80, 50, 35, 40, 68])
    dga_vals = np.array([2, 5, 8, 12, 6, 14, 19, 9, 3, 2, 4, 7])
    # normalize to box coordinates
    norm_x = 8 + (hrs - 0)/(24) * 80
    norm_y1 = 28 + (legit_vals / 120) * 30
    norm_y2 = 28 + (dga_vals / 120) * 30
    ax1.plot(norm_x, norm_y1, color='#0284c7', lw=2, label='Legit Traffic')
    ax1.plot(norm_x, norm_y2, color='#dc2626', lw=2, label='DGA Threats')
    ax1.text(50, 24, "Interval 2 Jam (Live Traffic Analytics via Chart.js)", ha='center', fontsize=7.5, color='#64748b')

    # Bottom Recent Incident Table Preview
    ax1.add_patch(patches.FancyBboxPatch((2, 2), 95, 16, boxstyle="round,pad=0.5", ec="#fca5a5", fc="#ffffff", lw=1))
    ax1.text(5, 13, "Temuan Ancaman C2 Terkini (Sinkholed):", fontsize=7.5, fontweight='bold', color='#dc2626')
    ax1.text(5, 7, "• xkq981mbpzwt74v.biz | H: 3.94 | Prob: 100% | Action: BLOCKED (SINKHOLE)\n• werbvnm1290zxc.ru   | H: 3.82 | Prob: 98.4%| Action: BLOCKED (SINKHOLE)",
             fontsize=7, color='#334155', fontfamily='monospace')

    # Panel 2: Single Domain Scanner Mockup
    ax2.set_facecolor('#f8fafc')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title("2. Tampilan Front-End: Single Domain Scanner (Instant)", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Input Box Mockup
    ax2.add_patch(patches.FancyBboxPatch((4, 78), 92, 16, boxstyle="round,pad=0.5", ec="#0284c7", fc="#ffffff", lw=1.5))
    ax2.text(8, 89, "Nama Domain / FQDN:", fontsize=7.5, fontweight='bold', color='#0284c7')
    ax2.text(8, 83, "xkq981mbpzwt74v.biz", fontsize=9.5, fontweight='bold', color='#0f172a', fontfamily='monospace')
    ax2.add_patch(patches.FancyBboxPatch((70, 80), 24, 10, boxstyle="round,pad=0.3", ec="#0284c7", fc="#0284c7"))
    ax2.text(82, 85, "Scan Now", ha='center', va='center', fontsize=8, fontweight='bold', color='#ffffff')

    # Verdict Result Banner
    ax2.add_patch(patches.FancyBboxPatch((4, 48), 92, 26, boxstyle="round,pad=0.5", ec="#fca5a5", fc="#fef2f2", lw=1.5))
    ax2.text(8, 67, "HASIL INFERENSI: DGA MALWARE THREAT (C2)", fontsize=9, fontweight='bold', color='#dc2626')
    ax2.text(8, 61, "Tingkat Keyakinan (Confidence): 100.0% | Probabilitas DGA: 1.000", fontsize=8, color='#0f172a')
    ax2.text(8, 55, "Mitigasi Otomatis: Dialihkan ke DNS Sinkhole (10.10.10.254) & Dropped", fontsize=8, color='#dc2626', fontweight='bold')
    ax2.add_patch(patches.Rectangle((8, 51), 84, 3, fc='#e2e8f0'))
    ax2.add_patch(patches.Rectangle((8, 51), 84, 3, fc='#dc2626'))

    # 4 Lexical Feature Cards (Colorful Pastel)
    feat_cards = [
        ("Length", "18 char", "#0284c7", "#f0f9ff", "#bae6fd", 4, 18),
        ("Vowel Ratio", "5.6%", "#7c3aed", "#f5f3ff", "#ddd6fe", 28, 18),
        ("Digit Ratio", "22.2%", "#059669", "#ecfdf5", "#a7f3d0", 52, 18),
        ("Shannon H", "3.9477", "#d97706", "#fffbeb", "#fde68a", 76, 18)
    ]
    for lbl, val, col, bg, bdc, x, y in feat_cards:
        ax2.add_patch(patches.FancyBboxPatch((x, y), 20, 24, boxstyle="round,pad=0.5", ec=bdc, fc=bg, lw=1.5))
        ax2.text(x+10, y+17, lbl, ha='center', va='center', fontsize=7.5, fontweight='bold', color=col)
        ax2.text(x+10, y+10, val, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f172a', fontfamily='monospace')
        ax2.text(x+10, y+4, "Feature Extr.", ha='center', va='center', fontsize=6.5, color='#64748b')

    # Quick Samples
    ax2.text(50, 8, "Sampel Uji Cepat: [bca.co.id (Legit)] [kemkes.go.id (Legit)] [suppobox.info (DGA)]", ha='center', fontsize=7.5, color='#475569')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_3_frontend_dashboard_scanner.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

# -------------------------------------------------------------
# 4. Visual Mockup: Batch Inspection & Real-Time Stream
# -------------------------------------------------------------
def create_ui_batch_stream():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)
    fig.patch.set_facecolor('#ffffff')

    # Panel 1: Batch Inspection Mockup
    ax1.set_facecolor('#f8fafc')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title("3. Tampilan Front-End: Batch Upload Inspection", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Upload Area
    ax1.add_patch(patches.FancyBboxPatch((4, 76), 92, 18, boxstyle="round,pad=0.5", ec="#0284c7", fc="#ffffff", lw=1.5))
    ax1.text(50, 88, "Unggah Berkas Log Jaringan (CSV, TXT, LOG, PCAP)", ha='center', fontsize=8.5, fontweight='bold', color='#0284c7')
    ax1.text(50, 81, "Pilih berkas log -> Ekstraksi leksikal & inferensi massal otomatis", ha='center', fontsize=7.5, color='#64748b')

    # Batch Stat Summary
    ax1.add_patch(patches.FancyBboxPatch((4, 56), 28, 16, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax1.text(18, 67, "TOTAL LOG", ha='center', fontsize=7, color='#64748b', fontweight='bold')
    ax1.text(18, 61, "300 Entri", ha='center', fontsize=11, fontweight='bold', color='#0f172a')

    ax1.add_patch(patches.FancyBboxPatch((36, 56), 28, 16, boxstyle="round,pad=0.5", ec="#fca5a5", fc="#fef2f2"))
    ax1.text(50, 67, "DGA THREATS", ha='center', fontsize=7, color='#dc2626', fontweight='bold')
    ax1.text(50, 61, "42 Terdeteksi", ha='center', fontsize=11, fontweight='bold', color='#dc2626')

    ax1.add_patch(patches.FancyBboxPatch((68, 56), 28, 16, boxstyle="round,pad=0.5", ec="#a7f3d0", fc="#ecfdf5"))
    ax1.text(82, 67, "LEGIT TRAFFIC", ha='center', fontsize=7, color='#059669', fontweight='bold')
    ax1.text(82, 61, "258 Aman", ha='center', fontsize=11, fontweight='bold', color='#059669')

    # Dynamic Filter Table Box
    ax1.add_patch(patches.FancyBboxPatch((4, 16), 92, 36, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax1.text(8, 46, "Filter: [Semua (300)] [Hanya DGA (42)] [Hanya Legit (258)]", fontsize=7.5, color='#0284c7', fontweight='bold')
    ax1.text(8, 40, "No  Domain Name              Entropy  Length  Status      Tindakan", fontsize=7, color='#64748b', fontfamily='monospace', fontweight='bold')
    ax1.text(8, 25, "1   xkq981mbpzwt74v.biz      3.94     18      DGA THREAT  SINKHOLE\n2   bca.co.id                2.41     9       LEGIT       ALLOWED\n3   werbvnm1290zxc.ru        3.82     17      DGA THREAT  SINKHOLE\n4   kemkes.go.id             2.72     12      LEGIT       ALLOWED",
             fontsize=7, color='#334155', fontfamily='monospace')

    # Export Buttons
    ax1.add_patch(patches.FancyBboxPatch((4, 4), 44, 8, boxstyle="round,pad=0.3", ec="#dc2626", fc="#dc2626"))
    ax1.text(26, 8, "Unduh Laporan Resmi (PDF)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#ffffff')
    ax1.add_patch(patches.FancyBboxPatch((52, 4), 44, 8, boxstyle="round,pad=0.3", ec="#475569", fc="#ffffff"))
    ax1.text(74, 8, "Ekspor Temuan (CSV/Excel)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#334155')

    # Panel 2: Real-Time DNS Stream Mockup
    ax2.set_facecolor('#f8fafc')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title("4. Tampilan Front-End: Real-Time DNS Stream", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Stream Controls Bar
    ax2.add_patch(patches.FancyBboxPatch((4, 80), 92, 14, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(8, 87, "Status: LIVE STREAMING (Polling 2.5s)", fontsize=8, fontweight='bold', color='#059669')
    ax2.text(8, 83, "Kueri aktif: 28 logs tertangkap | Latensi inferensi: 1.2 ms", fontsize=7.5, color='#64748b')
    ax2.add_patch(patches.FancyBboxPatch((60, 82), 16, 9, boxstyle="round,pad=0.2", ec="#d97706", fc="#fffbeb"))
    ax2.text(68, 86.5, "Pause", ha='center', va='center', fontsize=7, color='#d97706', fontweight='bold')
    ax2.add_patch(patches.FancyBboxPatch((78, 82), 16, 9, boxstyle="round,pad=0.2", ec="#0284c7", fc="#0284c7"))
    ax2.text(86, 86.5, "+ Simulate", ha='center', va='center', fontsize=7, color='#ffffff', fontweight='bold')

    # Live Feed Stream Table
    ax2.add_patch(patches.FancyBboxPatch((4, 6), 92, 70, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(8, 70, "Timestamp  Client IP     Domain Name             Entropy  Aksi", fontsize=7.5, color='#64748b', fontfamily='monospace', fontweight='bold')
    feed_lines = [
        "15:32:01   192.168.1.45  xkq981mbpzwt74v.biz     3.94     SINKHOLE (DROP)",
        "15:31:58   192.168.1.12  bca.co.id               2.41     ALLOWED",
        "15:31:54   10.0.10.88    werbvnm1290zxc.ru       3.82     SINKHOLE (DROP)",
        "15:31:49   192.168.1.80  kemkes.go.id            2.72     ALLOWED",
        "15:31:42   172.16.0.23   suppobox9912azq.info    3.79     SINKHOLE (DROP)",
        "15:31:35   192.168.1.55  tokopedia.com           2.80     ALLOWED",
        "15:31:30   192.168.1.99  necurs7723910vba.ru     3.85     SINKHOLE (DROP)",
        "15:31:22   10.0.10.15    detik.com               2.58     ALLOWED"
    ]
    y_pos = 62
    for line in feed_lines:
        col = '#dc2626' if 'SINKHOLE' in line else '#059669'
        ax2.text(8, y_pos, line, fontsize=7.2, color=col, fontfamily='monospace')
        y_pos -= 6.5

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_4_frontend_batch_stream.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

# -------------------------------------------------------------
# 5. Visual Mockup: Back-End Model Management & Threshold
# -------------------------------------------------------------
def create_ui_admin_model_threshold():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)
    fig.patch.set_facecolor('#ffffff')

    # Panel 1: Model Management & Visual Confusion Matrix
    ax1.set_facecolor('#f8fafc')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title("5. Tampilan Back-End: Model Management & Confusion Matrix", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # 4 Metric Cards
    metrics = [
        ("AKURASI", "87.59%", "#0284c7", "#f0f9ff", 4, 76),
        ("PRESISI", "93.79%", "#059669", "#ecfdf5", 28, 76),
        ("RECALL", "80.51%", "#d97706", "#fffbeb", 52, 76),
        ("F1-SCORE", "86.64%", "#7c3aed", "#f5f3ff", 76, 76)
    ]
    for lbl, val, col, bg, x, y in metrics:
        ax1.add_patch(patches.FancyBboxPatch((x, y), 20, 16, boxstyle="round,pad=0.5", ec=col, fc=bg, lw=1))
        ax1.text(x+10, y+11, lbl, ha='center', va='center', fontsize=7.5, fontweight='bold', color=col)
        ax1.text(x+10, y+4.5, val, ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')

    # Visual Confusion Matrix Grid 2x2
    ax1.add_patch(patches.FancyBboxPatch((4, 18), 92, 54, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax1.text(50, 67, "VISUAL CONFUSION MATRIX (1.652 SAMPEL EVALUASI)", ha='center', fontsize=8.5, fontweight='bold', color='#0f172a')

    # TP (665)
    ax1.add_patch(patches.FancyBboxPatch((12, 42), 36, 20, boxstyle="round,pad=0.5", ec="#a7f3d0", fc="#ecfdf5", lw=1.5))
    ax1.text(30, 56, "TRUE POSITIVE (TP)", ha='center', fontsize=8, fontweight='bold', color='#059669')
    ax1.text(30, 48, "665", ha='center', fontsize=14, fontweight='bold', color='#059669')
    ax1.text(30, 44, "DGA Terdeteksi Tepat", ha='center', fontsize=6.5, color='#64748b')

    # FP (44)
    ax1.add_patch(patches.FancyBboxPatch((52, 42), 36, 20, boxstyle="round,pad=0.5", ec="#fca5a5", fc="#fef2f2", lw=1.5))
    ax1.text(70, 56, "FALSE POSITIVE (FP)", ha='center', fontsize=8, fontweight='bold', color='#dc2626')
    ax1.text(70, 48, "44", ha='center', fontsize=14, fontweight='bold', color='#dc2626')
    ax1.text(70, 44, "Domain Sah Salah Blokir", ha='center', fontsize=6.5, color='#64748b')

    # FN (161)
    ax1.add_patch(patches.FancyBboxPatch((12, 20), 36, 20, boxstyle="round,pad=0.5", ec="#fde68a", fc="#fffbeb", lw=1.5))
    ax1.text(30, 34, "FALSE NEGATIVE (FN)", ha='center', fontsize=8, fontweight='bold', color='#d97706')
    ax1.text(30, 26, "161", ha='center', fontsize=14, fontweight='bold', color='#d97706')
    ax1.text(30, 22, "DGA Lolos (Missed)", ha='center', fontsize=6.5, color='#64748b')

    # TN (782)
    ax1.add_patch(patches.FancyBboxPatch((52, 20), 36, 20, boxstyle="round,pad=0.5", ec="#bae6fd", fc="#f0f9ff", lw=1.5))
    ax1.text(70, 34, "TRUE NEGATIVE (TN)", ha='center', fontsize=8, fontweight='bold', color='#0284c7')
    ax1.text(70, 26, "782", ha='center', fontsize=14, fontweight='bold', color='#0284c7')
    ax1.text(70, 22, "Domain Sah Diizinkan", ha='center', fontsize=6.5, color='#64748b')

    ax1.text(50, 7, "Catatan Evaluasi: Presisi tinggi (93.79%) menjamin kelancaran operasional bisnis.", ha='center', fontsize=7.5, color='#475569')

    # Panel 2: Decision Threshold Tuning Slider
    ax2.set_facecolor('#f8fafc')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title("6. Tampilan Back-End: Decision Threshold Tuning", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Current Threshold Display Card
    ax2.add_patch(patches.FancyBboxPatch((4, 60), 92, 34, boxstyle="round,pad=0.5", ec="#fde68a", fc="#ffffff", lw=1.5))
    ax2.text(50, 88, "AMBANG BATAS KEPUTUSAN AKTIF", ha='center', fontsize=8, fontweight='bold', color='#64748b')
    ax2.text(50, 78, "0.42", ha='center', fontsize=26, fontweight='bold', color='#d97706', fontfamily='monospace')
    ax2.text(50, 67, "Zona Optimal (0.40 - 0.42) - Sensitivitas Recall Maksimal", ha='center', fontsize=8, fontweight='bold', color='#059669')

    # Slider Mockup
    ax2.add_patch(patches.FancyBboxPatch((8, 48), 84, 4, boxstyle="round,pad=0.1", ec="#cbd5e1", fc="#e2e8f0"))
    ax2.add_patch(patches.FancyBboxPatch((8, 48), 35, 4, boxstyle="round,pad=0.1", ec="#d97706", fc="#d97706"))
    ax2.plot(43, 50, marker='o', markersize=12, color='#d97706', markeredgecolor='#ffffff', markeredgewidth=2)
    ax2.text(8, 43, "0.10 (Agresif)", fontsize=7, color='#64748b')
    ax2.text(43, 43, "0.42 (Optimal)", ha='center', fontsize=7.5, fontweight='bold', color='#d97706')
    ax2.text(92, 43, "0.90 (Ketat)", ha='right', fontsize=7, color='#64748b')

    # Explanatory Tradeoff
    ax2.add_patch(patches.FancyBboxPatch((4, 8), 92, 30, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(8, 32, "Analisis Trade-Off Sensitivitas:", fontsize=8, fontweight='bold', color='#0f172a')
    ax2.text(8, 25, "• Threshold < 0.40 : Recall mendekati 95%, namun risiko False Positive naik.", fontsize=7.2, color='#dc2626')
    ax2.text(8, 19, "• 0.40 <= Th <= 0.42 : Keseimbangan optimal (Recall 80.51% & Presisi 93.79%).", fontsize=7.2, color='#059669', fontweight='bold')
    ax2.text(8, 13, "• Threshold > 0.50 : Sangat aman, namun malware varian baru berisiko lolos.", fontsize=7.2, color='#0284c7')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_5_admin_model_threshold.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

# -------------------------------------------------------------
# 6. Visual Mockup: Firewall Sinkhole & Dataset Retrain
# -------------------------------------------------------------
def create_ui_admin_firewall_dataset():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)
    fig.patch.set_facecolor('#ffffff')

    # Panel 1: Firewall & Sinkhole Mockup
    ax1.set_facecolor('#f8fafc')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title("7. Tampilan Back-End: Firewall & DNS Sinkhole", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Sinkhole IP Box
    ax1.add_patch(patches.FancyBboxPatch((4, 76), 92, 18, boxstyle="round,pad=0.5", ec="#dc2626", fc="#ffffff", lw=1.5))
    ax1.text(8, 88, "Target IP DNS Sinkhole (Isolasi Jaringan):", fontsize=8, fontweight='bold', color='#dc2626')
    ax1.text(8, 81, "10.10.10.254 (Honeypot / Loopback)", fontsize=11, fontweight='bold', color='#0f172a', fontfamily='monospace')
    ax1.add_patch(patches.FancyBboxPatch((68, 79), 24, 10, boxstyle="round,pad=0.3", ec="#dc2626", fc="#dc2626"))
    ax1.text(80, 84, "Sync Rules", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#ffffff')

    # Export formats
    ax1.add_patch(patches.FancyBboxPatch((4, 52), 92, 20, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax1.text(8, 66, "Ekspor Format Aturan Perimeter:", fontsize=8, fontweight='bold', color='#0f172a')
    ax1.text(8, 58, "1. Linux IPTables Shell Script (.sh)\n2. BIND9 / RPZ Policy Zone (.zone)\n3. OS Hosts File (0.0.0.0 IP)\n4. pfSense / Fortinet URL Table (.txt)", fontsize=7.2, color='#475569')

    # Blacklist Table Preview
    ax1.add_patch(patches.FancyBboxPatch((4, 6), 92, 42, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax1.text(8, 42, "Daftar Cekal Aktif (Synchronized Blacklist):", fontsize=7.5, fontweight='bold', color='#dc2626')
    ax1.text(8, 35, "Domain                Detected At          Confidence  Action", fontsize=7, color='#64748b', fontfamily='monospace', fontweight='bold')
    ax1.text(8, 18, "xkq981mbpzwt74v.biz   2026-11-03 15:20:11  100.0%      SINKHOLED\nwerbvnm1290zxc.ru     2026-11-03 15:21:44  98.4%       SINKHOLED\nsuppobox9912azq.info  2026-11-03 15:22:05  94.2%       SINKHOLED\nnecurs7723910vba.ru   2026-11-03 15:23:18  97.6%       SINKHOLED",
             fontsize=7, color='#334155', fontfamily='monospace')

    # Panel 2: Dataset Management & Retrain
    ax2.set_facecolor('#f8fafc')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title("8. Tampilan Back-End: Dataset & Retraining Pipeline", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Corpus Stat Cards
    ax2.add_patch(patches.FancyBboxPatch((4, 76), 28, 18, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(18, 88, "TOTAL KORPUS", ha='center', fontsize=7, color='#64748b', fontweight='bold')
    ax2.text(18, 81, "1.338 Sampel", ha='center', fontsize=9.5, fontweight='bold', color='#0f172a')

    ax2.add_patch(patches.FancyBboxPatch((36, 76), 28, 18, boxstyle="round,pad=0.5", ec="#a7f3d0", fc="#ecfdf5"))
    ax2.text(50, 88, "DOMAIN SAH", ha='center', fontsize=7, color='#059669', fontweight='bold')
    ax2.text(50, 81, "638 Legit", ha='center', fontsize=9.5, fontweight='bold', color='#059669')

    ax2.add_patch(patches.FancyBboxPatch((68, 76), 28, 18, boxstyle="round,pad=0.5", ec="#fca5a5", fc="#fef2f2"))
    ax2.text(82, 88, "DOMAIN DGA", ha='center', fontsize=7, color='#dc2626', fontweight='bold')
    ax2.text(82, 81, "700 Botnet", ha='center', fontsize=9.5, fontweight='bold', color='#dc2626')

    # Upload & Retrain Controls
    ax2.add_patch(patches.FancyBboxPatch((4, 38), 92, 34, boxstyle="round,pad=0.5", ec="#7c3aed", fc="#ffffff", lw=1.5))
    ax2.text(8, 66, "Pembaruan Korpus & Siklus Pelatihan Ulang:", fontsize=8, fontweight='bold', color='#7c3aed')
    ax2.text(8, 59, "Unggah berkas dataset baru (.csv/.xlsx) untuk menambah varian botnet.\nSistem mengekstrak 4 fitur leksikal otomatis dan melatih 100 Decision Trees.", fontsize=7.2, color='#475569')
    ax2.add_patch(patches.FancyBboxPatch((8, 44), 40, 9, boxstyle="round,pad=0.3", ec="#7c3aed", fc="#7c3aed"))
    ax2.text(28, 48.5, "Picu Retraining Model", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#ffffff')
    ax2.add_patch(patches.FancyBboxPatch((52, 44), 40, 9, boxstyle="round,pad=0.3", ec="#475569", fc="#ffffff"))
    ax2.text(72, 48.5, "Ekspor Dataset Excel", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#334155')

    # Corpus Preview Table
    ax2.add_patch(patches.FancyBboxPatch((4, 6), 92, 28, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(8, 29, "Pratinjau Data Latihan (Top 25):", fontsize=7.5, fontweight='bold', color='#0f172a')
    ax2.text(8, 23, "Domain                  Length  Vowel   Digit   Entropy  Label", fontsize=7, color='#64748b', fontfamily='monospace', fontweight='bold')
    ax2.text(8, 12, "google.com              10      40.0%   0.0%    2.6464   0 (Legit)\nxkq981mbpzwt74v.biz     18      5.6%    22.2%   3.9477   1 (DGA)\nbca.co.id               9       33.3%   0.0%    2.4194   0 (Legit)",
             fontsize=7, color='#334155', fontfamily='monospace')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_6_admin_firewall_dataset.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

# -------------------------------------------------------------
# 7. Visual Mockup: API/Webhook, Health, & Audit Trail
# -------------------------------------------------------------
def create_ui_admin_api_health():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)
    fig.patch.set_facecolor('#ffffff')

    # Panel 1: API & Webhooks Mockup
    ax1.set_facecolor('#f8fafc')
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.axis('off')
    ax1.set_title("9. Tampilan Back-End: API & Webhook Management", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # API Keys Card
    ax1.add_patch(patches.FancyBboxPatch((4, 52), 92, 42, boxstyle="round,pad=0.5", ec="#0284c7", fc="#ffffff", lw=1.5))
    ax1.text(8, 88, "Otorisasi API Key Eksternal (X-API-Key):", fontsize=8, fontweight='bold', color='#0284c7')
    ax1.text(8, 81, "Endpoint: POST /api/v1/detect (JSON / cURL)", fontsize=7.5, color='#475569')
    ax1.text(8, 73, "Klien / Layanan          API Token 256-bit             Status", fontsize=7, color='#64748b', fontfamily='monospace', fontweight='bold')
    ax1.text(8, 62, "Firewall Gateway L3      soc-dga-live-key-9921         ACTIVE\nEdge Sniffer Sensor      soc_dga_7a8109bfbc8210e       ACTIVE", fontsize=7, color='#334155', fontfamily='monospace')

    # Webhook Alert Card
    ax1.add_patch(patches.FancyBboxPatch((4, 6), 92, 42, boxstyle="round,pad=0.5", ec="#dc2626", fc="#ffffff", lw=1.5))
    ax1.text(8, 42, "Penyalur Notifikasi Instan (Webhook Alerting):", fontsize=8, fontweight='bold', color='#dc2626')
    ax1.text(8, 35, "Platform: Discord Channel SOC / Telegram Incident Bot\nAmbang Peringatan: Kritis (P(DGA) >= 0.70)\nURL: https://discord.com/api/webhooks/soc-alert-channel", fontsize=7.2, color='#475569')
    ax1.add_patch(patches.FancyBboxPatch((8, 14), 40, 9, boxstyle="round,pad=0.3", ec="#d97706", fc="#fffbeb"))
    ax1.text(28, 18.5, "Uji Kirim Webhook", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#d97706')

    # Panel 2: System Health & Audit Trail Mockup
    ax2.set_facecolor('#f8fafc')
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 100)
    ax2.axis('off')
    ax2.set_title("10. Tampilan Back-End: Health & Immutable Audit Trail", fontsize=11, fontweight='bold', color='#0f172a', pad=12)

    # Health Metrics Box
    ax2.add_patch(patches.FancyBboxPatch((4, 54), 92, 40, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(8, 88, "Status Infrastruktur Server & Latensi Inferensi:", fontsize=8, fontweight='bold', color='#0f172a')
    ax2.text(8, 80, "CPU: 12.4%  |  RAM: 4.8 / 16 GB (30%)  |  Disk: 42 GB Free\nInference Latency: 1.2 ms / query (Sub-millisecond Real-Time)", fontsize=7.5, color='#0284c7', fontweight='bold')
    ax2.text(8, 68, "• DNS Capture Engine   : OPERATIONAL (Listening)\n• ML Inference Daemon  : ACTIVE (Random Forest Ready)\n• Database Storage     : ONLINE (SQLite WAL Mode)\n• Firewall Sync Daemon : ACTIVE (Target: 10.10.10.254)", fontsize=7, color='#334155')

    # Audit Trail Table
    ax2.add_patch(patches.FancyBboxPatch((4, 6), 92, 44, boxstyle="round,pad=0.5", ec="#e2e8f0", fc="#ffffff"))
    ax2.text(8, 44, "Immutable Audit Trail Log (Kepatuhan Regulasi ISO 27001):", fontsize=7.5, fontweight='bold', color='#0f172a')
    ax2.text(8, 38, "Timestamp  User     Role     Action           Details", fontsize=7, color='#64748b', fontfamily='monospace', fontweight='bold')
    ax2.text(8, 18, "15:20:11   analyst  analyst  Single Scan      Domain xkq981 scanned: DGA (100%)\n15:18:05   admin    admin    Threshold Tuning Decision threshold set to 0.42\n15:15:30   admin    admin    Firewall Sync    6 rules exported to Sinkhole\n15:12:00   admin    admin    Retrain Pipeline Model Random Forest retrained",
             fontsize=6.8, color='#334155', fontfamily='monospace')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, 'gambar_7_admin_api_health_audit.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved {out_path}")

if __name__ == '__main__':
    print("[*] Generating high-resolution visual report assets...")
    create_architecture_diagram()
    create_erd_diagram()
    create_ui_dashboard_scanner()
    create_ui_batch_stream()
    create_ui_admin_model_threshold()
    create_ui_admin_firewall_dataset()
    create_ui_admin_api_health()
    print("[*] All 7 visual assets generated successfully!")
