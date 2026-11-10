import os
import re
import sqlite3
import mysql.connector

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
    try:
        raw = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dga_detection_system",
            autocommit=True
        )
        return DBConnectionWrapper(raw, 'mysql')
    except Exception as e:
        print("[!] MySQL connection failed, fallback to SQLite:", e)
        raw_sq = sqlite3.connect("database.db")
        raw_sq.row_factory = sqlite3.Row
        return DBConnectionWrapper(raw_sq, 'sqlite')

if __name__ == "__main__":
    db = get_db()
    print("Database connected. Type:", db.db_type)
    r = db.execute("SELECT COUNT(*) as cnt FROM dataset").fetchone()
    print("Dataset count:", r['cnt'])
    s = db.execute("SELECT value FROM settings WHERE key = ?", ('threshold',)).fetchone()
    print("Threshold setting:", s['value'])
    m = db.execute("SELECT * FROM model_metrics ORDER BY id DESC LIMIT 1").fetchone()
    print("Accuracy:", m['accuracy'])
    db.close()
