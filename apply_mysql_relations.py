import mysql.connector

def apply_relations():
    print("[1] Connecting to MySQL dga_detection_system...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dga_detection_system",
        autocommit=True
    )
    cur = conn.cursor(dictionary=True)

    print("[2] Adding Foreign Key columns...")

    # Helper function to add column if not exists
    def add_col_if_missing(table, col_def, col_name):
        cur.execute(f"SHOW COLUMNS FROM {table} LIKE '{col_name}'")
        if not cur.fetchone():
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
            print(f"  [+] Added column `{col_name}` to `{table}`")
        else:
            print(f"  [-] Column `{col_name}` already exists in `{table}`")

    add_col_if_missing("audit_logs", "user_id INT NULL AFTER role", "user_id")
    add_col_if_missing("api_keys", "user_id INT NULL AFTER id", "user_id")
    add_col_if_missing("model_metrics", "trained_by_user_id INT NULL AFTER id", "trained_by_user_id")
    add_col_if_missing("dataset", "uploaded_by_user_id INT NULL", "uploaded_by_user_id")
    add_col_if_missing("blocked_domains", "dns_log_id INT NULL AFTER id", "dns_log_id")
    add_col_if_missing("dns_logs", "api_key_id INT NULL AFTER id", "api_key_id")

    print("[3] Populating initial relational linkage data...")

    # Link audit_logs to users
    cur.execute("UPDATE audit_logs SET user_id = 2 WHERE user = 'admin' OR user LIKE '%admin%'")
    cur.execute("UPDATE audit_logs SET user_id = 1 WHERE user = 'analyst' OR user_id IS NULL")

    # Link api_keys to admin user (id=2)
    cur.execute("UPDATE api_keys SET user_id = 2 WHERE user_id IS NULL")

    # Link model_metrics to admin user (id=2)
    cur.execute("UPDATE model_metrics SET trained_by_user_id = 2 WHERE trained_by_user_id IS NULL")

    # Link dataset to admin user (id=2)
    cur.execute("UPDATE dataset SET uploaded_by_user_id = 2 WHERE uploaded_by_user_id IS NULL")

    # Link blocked_domains to dns_logs
    cur.execute("""
    UPDATE blocked_domains bd
    JOIN dns_logs dl ON bd.domain = dl.domain
    SET bd.dns_log_id = dl.id
    WHERE bd.dns_log_id IS NULL
    """)

    # Link api_key_id in dns_logs for simulated api / stream
    cur.execute("UPDATE dns_logs SET api_key_id = 1 WHERE id % 3 = 0")

    print("[4] Applying explicit FOREIGN KEY constraints for phpMyAdmin Designer...")

    fk_definitions = [
        ("audit_logs", "fk_audit_user", "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE"),
        ("api_keys", "fk_api_user", "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE"),
        ("model_metrics", "fk_model_user", "FOREIGN KEY (trained_by_user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE"),
        ("dataset", "fk_dataset_user", "FOREIGN KEY (uploaded_by_user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE"),
        ("blocked_domains", "fk_blocked_dns_log", "FOREIGN KEY (dns_log_id) REFERENCES dns_logs(id) ON DELETE SET NULL ON UPDATE CASCADE"),
        ("dns_logs", "fk_dns_api_key", "FOREIGN KEY (api_key_id) REFERENCES api_keys(id) ON DELETE SET NULL ON UPDATE CASCADE")
    ]

    for table, fk_name, fk_rule in fk_definitions:
        # Check if constraint exists
        cur.execute(f"""
        SELECT CONSTRAINT_NAME 
        FROM information_schema.TABLE_CONSTRAINTS 
        WHERE TABLE_SCHEMA = 'dga_detection_system' 
          AND TABLE_NAME = '{table}' 
          AND CONSTRAINT_NAME = '{fk_name}'
        """)
        if not cur.fetchone():
            try:
                cur.execute(f"ALTER TABLE {table} ADD CONSTRAINT {fk_name} {fk_rule}")
                print(f"  [+] Constraint `{fk_name}` on `{table}` added successfully!")
            except Exception as e:
                print(f"  [!] Failed to add constraint `{fk_name}`: {e}")
        else:
            print(f"  [-] Constraint `{fk_name}` already active on `{table}`")

    print("\n[5] Verifying active Foreign Keys in database:")
    cur.execute("""
    SELECT 
        TABLE_NAME, 
        COLUMN_NAME, 
        CONSTRAINT_NAME, 
        REFERENCED_TABLE_NAME, 
        REFERENCED_COLUMN_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = 'dga_detection_system' 
      AND REFERENCED_TABLE_NAME IS NOT NULL
    """)
    active_fks = cur.fetchall()
    for fk in active_fks:
        print(f"  * {fk['TABLE_NAME']}.{fk['COLUMN_NAME']} -> {fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']} ({fk['CONSTRAINT_NAME']})")

    conn.close()
    print("\n[SUCCESS] Relasi Foreign Key MySQL berhasil dibuat! Garis relasi di phpMyAdmin Designer kini aktif.")

if __name__ == "__main__":
    apply_relations()
