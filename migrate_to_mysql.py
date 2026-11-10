import sqlite3
import mysql.connector

SQLITE_PATH = "database.db"

def migrate():
    print("[1] Connecting to MySQL on localhost:3306...")
    conn_root = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        autocommit=True
    )
    cursor_root = conn_root.cursor()
    cursor_root.execute("CREATE DATABASE IF NOT EXISTS dga_detection_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("[+] Database 'dga_detection_system' created or verified.")
    conn_root.close()

    conn_mysql = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dga_detection_system",
        autocommit=True
    )
    cur = conn_mysql.cursor()

    # Create Tables
    print("[2] Creating MySQL tables...")

    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute('''
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(64) UNIQUE,
        full_name VARCHAR(128),
        role VARCHAR(32),
        status VARCHAR(32)
    ) ENGINE=InnoDB;
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        `key` VARCHAR(64) PRIMARY KEY,
        `value` TEXT
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS model_metrics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        accuracy FLOAT,
        `precision` FLOAT,
        recall FLOAT,
        f1_score FLOAT,
        threshold FLOAT,
        cm_tp INT,
        cm_fp INT,
        cm_fn INT,
        cm_tn INT,
        last_trained VARCHAR(64)
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS dns_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp VARCHAR(64),
        source_ip VARCHAR(64),
        domain VARCHAR(255),
        entropy FLOAT,
        length INT,
        vowel_ratio FLOAT,
        digit_ratio FLOAT,
        dga_probability FLOAT,
        classification VARCHAR(32),
        action_taken VARCHAR(32),
        INDEX idx_domain (domain),
        INDEX idx_class (classification)
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS blocked_domains (
        id INT AUTO_INCREMENT PRIMARY KEY,
        domain VARCHAR(255) UNIQUE,
        detected_at VARCHAR(64),
        threat_type VARCHAR(64),
        confidence FLOAT,
        status VARCHAR(32)
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS dataset (
        id INT AUTO_INCREMENT PRIMARY KEY,
        domain VARCHAR(255),
        length INT,
        vowel_ratio FLOAT,
        digit_ratio FLOAT,
        shannon_entropy FLOAT,
        label INT,
        source VARCHAR(64),
        INDEX idx_label (label)
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INT AUTO_INCREMENT PRIMARY KEY,
        key_name VARCHAR(64),
        api_key VARCHAR(128) UNIQUE,
        created_at VARCHAR(64),
        last_used VARCHAR(64),
        status VARCHAR(32)
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(64) UNIQUE,
        full_name VARCHAR(128),
        role VARCHAR(32),
        status VARCHAR(32)
    ) ENGINE=InnoDB;
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp VARCHAR(64),
        user VARCHAR(64),
        role VARCHAR(32),
        action VARCHAR(64),
        details TEXT,
        ip_address VARCHAR(64)
    ) ENGINE=InnoDB;
    ''')

    print("[+] All 8 MySQL tables ready.")

    # Migrate Data from SQLite
    print("[3] Migrating data from SQLite (database.db)...")
    conn_sq = sqlite3.connect(SQLITE_PATH)
    conn_sq.row_factory = sqlite3.Row
    cur_sq = conn_sq.cursor()

    tables = [
        "settings",
        "model_metrics",
        "dns_logs",
        "blocked_domains",
        "dataset",
        "api_keys",
        "users",
        "audit_logs"
    ]

    for tbl in tables:
        # Check SQLite rows
        rows = cur_sq.execute(f"SELECT * FROM {tbl}").fetchall()
        if not rows:
            print(f"  - Table {tbl}: 0 rows in SQLite, skipping.")
            continue

        # Clear existing rows in MySQL to prevent duplicate key errors on fresh migration
        cur.execute(f"TRUNCATE TABLE {tbl}")

        # Get column names
        cols = list(rows[0].keys())
        # Format for MySQL
        cols_quoted = [f"`{c}`" if c in ("key", "precision") else c for c in cols]
        cols_str = ", ".join(cols_quoted)
        placeholders = ", ".join(["%s"] * len(cols))
        sql = f"INSERT INTO {tbl} ({cols_str}) VALUES ({placeholders})"

        data_to_insert = [tuple(r[c] for c in cols) for r in rows]
        cur.executemany(sql, data_to_insert)
        print(f"  [+] Migrated {len(data_to_insert)} rows into MySQL `{tbl}`.")

    conn_sq.close()
    conn_mysql.close()
    print("\n[SUCCESS] Migration to MySQL 'dga_detection_system' completed successfully!")

if __name__ == "__main__":
    migrate()
