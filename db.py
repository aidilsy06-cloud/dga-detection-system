import os
import re
import sqlite3
import mysql.connector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(BASE_DIR, 'database.db')

MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DB', 'dga_detection_system'),
    'autocommit': True
}

class MySQLCursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @property
    def rowcount(self):
        return self.cursor.rowcount

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

class DBConnectionWrapper:
    def __init__(self, cnx, db_type='mysql'):
        self.cnx = cnx
        self.db_type = db_type

    def _normalize_sql(self, sql):
        if self.db_type == 'mysql':
            # Replace sqlite placeholder ? with %s
            sql = sql.replace('?', '%s')
            # Replace INSERT OR IGNORE with INSERT IGNORE
            sql = re.sub(r'INSERT\s+OR\s+IGNORE\s+INTO', 'INSERT IGNORE INTO', sql, flags=re.IGNORECASE)
            # Replace INSERT OR REPLACE with REPLACE
            sql = re.sub(r'INSERT\s+OR\s+REPLACE\s+INTO', 'REPLACE INTO', sql, flags=re.IGNORECASE)
            # Quote reserved words in table/column names
            sql = re.sub(r'\bWHERE\s+key\s*=', 'WHERE `key` =', sql, flags=re.IGNORECASE)
            sql = re.sub(r'\(key,\s*value\)', '(`key`, `value`)', sql, flags=re.IGNORECASE)
            sql = re.sub(r'settings\s+SET\s+value\s*=\s*%s\s+WHERE\s+key\s*=', 'settings SET `value` = %s WHERE `key` =', sql, flags=re.IGNORECASE)
            sql = re.sub(r'settings\s+SET\s+value\s*=\s*\?\s+WHERE\s+key\s*=', 'settings SET `value` = %s WHERE `key` =', sql, flags=re.IGNORECASE)
            # Handle MySQL delete with subquery on same table
            if 'DELETE FROM dns_logs WHERE id NOT IN (SELECT id FROM dns_logs' in sql:
                sql = "DELETE FROM dns_logs WHERE id NOT IN (SELECT id FROM (SELECT id FROM dns_logs ORDER BY id DESC LIMIT 5) as _tmp)"
        return sql

    def execute(self, sql, params=None):
        if self.db_type == 'sqlite':
            if params is not None:
                return self.cnx.execute(sql, params)
            return self.cnx.execute(sql)
        else:
            cur = self.cnx.cursor(dictionary=True)
            norm_sql = self._normalize_sql(sql)
            if params is not None:
                cur.execute(norm_sql, params)
            else:
                cur.execute(norm_sql)
            return MySQLCursorWrapper(cur)

    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def close(self):
        self.cnx.close()

def get_db():
    """
    Koneksi Database Utama: MySQL (XAMPP localhost:3306)
    Jika MySQL tidak aktif / tidak tersedia, otomatis fallback ke SQLite (database.db)
    sehingga sistem tetap berjalan stabil dalam kondisi apapun.
    """
    try:
        raw_mysql = mysql.connector.connect(**MYSQL_CONFIG)
        return DBConnectionWrapper(raw_mysql, 'mysql')
    except Exception as e:
        # Fallback to SQLite
        raw_sqlite = sqlite3.connect(SQLITE_PATH)
        raw_sqlite.row_factory = sqlite3.Row
        return DBConnectionWrapper(raw_sqlite, 'sqlite')

def get_db_info():
    db = get_db()
    info = {
        'type': db.db_type.upper(),
        'target': f"MySQL ({MYSQL_CONFIG['user']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']})" if db.db_type == 'mysql' else f"SQLite ({SQLITE_PATH})",
        'is_mysql': db.db_type == 'mysql'
    }
    db.close()
    return info
