import sqlite3

DB_NAME = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS processed (
        tx_hash TEXT PRIMARY KEY
    )
    """)
    conn.commit()
    conn.close()

def exists(tx_hash):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT tx_hash FROM processed WHERE tx_hash=?", (tx_hash,))
    row = cur.fetchone()
    conn.close()
    return row is not None

def save(tx_hash):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO processed(tx_hash) VALUES(?)", (tx_hash,))
    conn.commit()
    conn.close()