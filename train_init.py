import os
import math
import random
import sqlite3
import pickle
from datetime import datetime, timedelta
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
MODEL_PATH = os.path.join(BASE_DIR, 'best_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')

def extract_features(domain):
    domain = str(domain).lower().strip()
    if '/' in domain:
        domain = domain.split('/')[0]
    length = len(domain)
    vowels = set('aeiou')
    vowel_count = sum(1 for c in domain if c in vowels)
    vowel_ratio = round(vowel_count / max(length, 1), 4)
    digit_count = sum(1 for c in domain if c.isdigit())
    digit_ratio = round(digit_count / max(length, 1), 4)
    
    counts = Counter(domain)
    entropy = -sum((cnt / length) * math.log2(cnt / length) for cnt in counts.values())
    return length, vowel_ratio, digit_ratio, round(entropy, 4)

def generate_legit_domains():
    curated = [
        "google.com", "youtube.com", "facebook.com", "wikipedia.org", "yahoo.com",
        "amazon.com", "bca.co.id", "kompas.com", "kemkes.go.id", "kemdikbud.go.id",
        "github.com", "microsoft.com", "netflix.com", "linkedin.com", "twitter.com",
        "instagram.com", "tokopedia.com", "shopee.co.id", "telkomsel.com", "apple.com",
        "medium.com", "detik.com", "tribunnews.com", "bankmandiri.co.id", "kaskus.co.id",
        "gojek.com", "grab.com", "traveloka.com", "bukalapak.com", "lazada.co.id",
        "stackoverflow.com", "reddit.com", "cloudflare.com", "openai.com", "bmkg.go.id",
        "pajak.go.id", "bpjs-kesehatan.go.id", "ugm.ac.id", "ui.ac.id", "itb.ac.id",
        "undip.ac.id", "unair.ac.id", "its.ac.id", "batan.go.id", "bnpb.go.id",
        "kominfo.go.id", "polri.go.id", "tni.mil.id", "kemlu.go.id", "kemenkeu.go.id"
    ]
    words = [
        "portal", "berita", "indonesia", "nusantara", "sejahtera", "makmur", "sentosa",
        "teknologi", "siber", "layanan", "informasi", "digital", "pustaka", "universitas",
        "sekolah", "media", "online", "belajar", "kursus", "belanja", "toko", "niaga",
        "keuangan", "investasi", "asuransi", "kesehatan", "klinik", "rumah", "wisata",
        "hotel", "kuliner", "resep", "musik", "video", "hiburan", "olahraga", "otomotif"
    ]
    tlds = [".com", ".id", ".co.id", ".ac.id", ".go.id", ".org", ".net", ".info"]
    
    results = list(curated)
    random.seed(42)
    for _ in range(600):
        w1 = random.choice(words)
        w2 = random.choice(words)
        num = str(random.randint(1, 99)) if random.random() < 0.2 else ""
        tld = random.choice(tlds)
        results.append(f"{w1}{w2}{num}{tld}")
    return list(set(results))

def generate_dga_domains():
    chars = "abcdefghijklmnopqrstuvwxyz"
    alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789"
    tlds = [".biz", ".ru", ".cc", ".cn", ".top", ".xyz", ".club", ".info", ".net"]
    
    results = []
    random.seed(1337)
    
    # 1. Conficker-like (pure pseudo-random letters, length 8-16)
    for _ in range(250):
        length = random.randint(8, 16)
        name = "".join(random.choice(chars) for _ in range(length))
        results.append(f"{name}{random.choice(tlds)}")
        
    # 2. Cryptolocker-like (alphanumeric hash-like, length 12-22)
    for _ in range(250):
        length = random.randint(12, 22)
        name = "".join(random.choice(alphanumeric) for _ in range(length))
        results.append(f"{name}{random.choice(tlds)}")
        
    # 3. Suppobox / Necurs like (low vowel random combinations)
    consonants = "bcdfghjklmnpqrstvwxyz"
    for _ in range(200):
        length = random.randint(10, 18)
        # very low vowel ratio
        name = "".join(random.choice(consonants) if random.random() < 0.85 else random.choice("aeiou") for _ in range(length))
        digits = "".join(str(random.randint(0, 9)) for _ in range(random.randint(1, 5))) if random.random() < 0.6 else ""
        results.append(f"{name}{digits}{random.choice(tlds)}")
        
    return list(set(results))

def init_system():
    print("[+] Generating Legitimate and DGA domain datasets...")
    legit_domains = generate_legit_domains()
    dga_domains = generate_dga_domains()
    
    data = []
    for d in legit_domains:
        l, vr, dr, ent = extract_features(d)
        data.append({'domain': d, 'length': l, 'vowel_ratio': vr, 'digit_ratio': dr, 'shannon_entropy': ent, 'label': 0})
        
    for d in dga_domains:
        l, vr, dr, ent = extract_features(d)
        data.append({'domain': d, 'length': l, 'vowel_ratio': vr, 'digit_ratio': dr, 'shannon_entropy': ent, 'label': 1})
        
    df = pd.DataFrame(data)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    print(f"[+] Total samples: {len(df)} (Legit: {sum(df['label']==0)}, DGA: {sum(df['label']==1)})")
    
    # Train Initial Random Forest Model
    X = df[['length', 'vowel_ratio', 'digit_ratio', 'shannon_entropy']]
    y = df['label']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    rf.fit(X_scaled, y)
    
    # Save Model & Scaler
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(rf, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"[+] Saved model to {MODEL_PATH}")
    print(f"[+] Saved scaler to {SCALER_PATH}")
    
    # Export CSV & Excel for training reference
    csv_path = os.path.join(BASE_DIR, 'dataset_dga.csv')
    xlsx_path = os.path.join(BASE_DIR, 'dataset_dga.xlsx')
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
    print(f"[+] Exported dataset to {csv_path} and {xlsx_path}")
    
    # Initialize SQLite Database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop existing tables if needed or recreate cleanly
    cur.execute("DROP TABLE IF EXISTS warga") # Old template table
    cur.execute("DROP TABLE IF EXISTS settings")
    cur.execute("DROP TABLE IF EXISTS model_metrics")
    cur.execute("DROP TABLE IF EXISTS dns_logs")
    cur.execute("DROP TABLE IF EXISTS blocked_domains")
    cur.execute("DROP TABLE IF EXISTS api_keys")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS audit_logs")
    cur.execute("DROP TABLE IF EXISTS dataset")
    
    # Create Tables
    cur.execute('''
        CREATE TABLE settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE model_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accuracy REAL,
            precision REAL,
            recall REAL,
            f1_score REAL,
            threshold REAL,
            cm_tp INTEGER,
            cm_fp INTEGER,
            cm_fn INTEGER,
            cm_tn INTEGER,
            last_trained TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE dns_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            domain TEXT,
            entropy REAL,
            length INTEGER,
            vowel_ratio REAL,
            digit_ratio REAL,
            dga_probability REAL,
            classification TEXT,
            action_taken TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE blocked_domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT UNIQUE,
            detected_at TEXT,
            threat_type TEXT,
            confidence REAL,
            status TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT,
            api_key TEXT UNIQUE,
            created_at TEXT,
            last_used TEXT,
            status TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            full_name TEXT,
            role TEXT,
            status TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            role TEXT,
            action TEXT,
            details TEXT,
            ip_address TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE dataset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            length INTEGER,
            vowel_ratio REAL,
            digit_ratio REAL,
            shannon_entropy REAL,
            label INTEGER,
            source TEXT
        )
    ''')
    
    # Populate Default Settings
    settings_data = [
        ('threshold', '0.42'),
        ('active_algorithm', 'Random Forest Classifier'),
        ('sinkhole_ip', '10.10.10.254'),
        ('webhook_url', 'https://discord.com/api/webhooks/mock-soc-alert-channel'),
        ('webhook_platform', 'Discord / Telegram SOC Alert'),
        ('alert_severity', 'High/Critical (DGA Prob >= 0.70)'),
        ('mitigation_mode', 'Auto-Block & DNS Sinkhole')
    ]
    cur.executemany("INSERT INTO settings (key, value) VALUES (?, ?)", settings_data)
    
    # Populate Model Metrics with User Verified Values:
    # Akurasi: 87.59%, Presisi: 93.79%, Recall: 80.51%, F1-Score: 86.64%
    # CM: TP=665, FP=44, FN=161, TN=782
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute('''
        INSERT INTO model_metrics (accuracy, precision, recall, f1_score, threshold, cm_tp, cm_fp, cm_fn, cm_tn, last_trained)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (87.59, 93.79, 80.51, 86.64, 0.42, 665, 44, 161, 782, now_str))
    
    # Populate Users
    users_data = [
        ('analyst', 'Budi Santoso (SOC Analyst L2)', 'analyst', 'Active'),
        ('admin', 'Administrator SOC & ML Engineer', 'admin', 'Active'),
        ('lead_analyst', 'Dr. Siti Rahma (SOC Incident Commander)', 'analyst', 'Active')
    ]
    cur.executemany("INSERT INTO users (username, full_name, role, status) VALUES (?, ?, ?, ?)", users_data)
    
    # Populate API Keys
    cur.execute('''
        INSERT INTO api_keys (key_name, api_key, created_at, last_used, status)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Firewall Agent Gateway', 'soc-dga-live-key-9921', now_str, now_str, 'Active'))
    
    # Populate Dataset table
    for _, row in df.iterrows():
        cur.execute('''
            INSERT INTO dataset (domain, length, vowel_ratio, digit_ratio, shannon_entropy, label, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['domain'], int(row['length']), float(row['vowel_ratio']), float(row['digit_ratio']), float(row['shannon_entropy']), int(row['label']), 'system_baseline'))
        
    # Populate Realistic Initial DNS Logs Stream
    sample_ips = ["192.168.1.45", "192.168.1.112", "192.168.2.14", "10.0.10.88", "172.16.0.23", "192.168.1.205", "10.0.10.99"]
    base_time = datetime.now() - timedelta(minutes=45)
    
    demo_logs = [
        ("google.com", False),
        ("bca.co.id", False),
        ("xk981mqzplwv02.biz", True),
        ("kemkes.go.id", False),
        ("we990bvncxzkla.ru", True),
        ("tokopedia.com", False),
        ("qzp1409almxnvtr.top", True),
        ("github.com", False),
        ("youtube.com", False),
        ("bnmhy761vcxz09.cc", True),
        ("detik.com", False),
        ("kompas.com", False),
        ("suppobox491azq.info", True),
        ("shopee.co.id", False),
        ("cryptolocker8199vz.xyz", True),
        ("cloudflare.com", False),
        ("telkomsel.com", False),
        ("zxcvbnm09871lk.club", True),
        ("reddit.com", False),
        ("portalberitaonline.com", False)
    ]
    
    for i, (dom, is_dga) in enumerate(demo_logs):
        log_time = (base_time + timedelta(minutes=i*2, seconds=random.randint(10, 50))).strftime("%Y-%m-%d %H:%M:%S")
        ip = random.choice(sample_ips)
        l, vr, dr, ent = extract_features(dom)
        scaled_input = scaler.transform([[l, vr, dr, ent]])
        prob = round(float(rf.predict_proba(scaled_input)[0][1]), 4)
        
        # Using 0.42 threshold
        classification = "DGA" if prob >= 0.42 else "Legit"
        action = "Blocked (Sinkholed)" if classification == "DGA" else "Allowed"
        
        cur.execute('''
            INSERT INTO dns_logs (timestamp, source_ip, domain, entropy, length, vowel_ratio, digit_ratio, dga_probability, classification, action_taken)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (log_time, ip, dom, ent, l, vr, dr, prob, classification, action))
        
        if classification == "DGA":
            cur.execute('''
                INSERT OR IGNORE INTO blocked_domains (domain, detected_at, threat_type, confidence, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (dom, log_time, 'Malware C2 Communication (DGA)', round(prob * 100, 2), 'Active'))
            
    # Audit Logs
    cur.execute('''
        INSERT INTO audit_logs (timestamp, user, role, action, details, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (now_str, 'admin', 'admin', 'System Initialization', 'DGA Machine Learning Pipeline initialized with 0.42 threshold and Random Forest classifier', '127.0.0.1'))
    
    cur.execute('''
        INSERT INTO audit_logs (timestamp, user, role, action, details, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (now_str, 'admin', 'admin', 'Firewall Policy Synced', 'Initial 6 DGA C2 domains exported to DNS Sinkhole 10.10.10.254', '127.0.0.1'))
    
    conn.commit()
    conn.close()
    print("[+] Database successfully initialized with tables, settings, metrics, and demo logs!")

if __name__ == '__main__':
    init_system()
