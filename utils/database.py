import sqlite3
import os
from datetime import datetime, timedelta

# Railway'da volume yo'li, yo'q bo'lsa lokal papka
if os.path.exists("/data"):
    DB_PATH = "/data/hymind.db"
else:
    DB_PATH = "hymind.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Foydalanuvchilar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            premium_until TEXT,
            pomodoro_cycles INTEGER DEFAULT 0,
            total_pomodoro_minutes INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Promo-kodlar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promo_codes (
            code TEXT PRIMARY KEY,
            bonus_days INTEGER,
            max_uses INTEGER DEFAULT 1,
            used_count INTEGER DEFAULT 0,
            expires_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Promo-kod ishlatish tarixi
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promo_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            code TEXT,
            used_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (code) REFERENCES promo_codes(code)
        )
    """)
    
    # Musiqalar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT NOT NULL,
            caption TEXT,
            file_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # So'zlar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def create_user(user_id, username, first_name):
    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user_id, username, first_name)
    )
    conn.commit()
    conn.close()

def get_premium_until(user_id):
    conn = get_db()
    result = conn.execute(
        "SELECT premium_until FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    if result and result["premium_until"]:
        return datetime.fromisoformat(result["premium_until"])
    return None

def is_premium(user_id):
    premium_until = get_premium_until(user_id)
    if not premium_until:
        return False
    return premium_until > datetime.now()

def get_premium_days_left(user_id):
    premium_until = get_premium_until(user_id)
    if not premium_until:
        return 0
    delta = premium_until - datetime.now()
    return max(0, delta.days)

def extend_premium(user_id, days):
    conn = get_db()
    current = get_premium_until(user_id)
    
    if current and current > datetime.now():
        new_date = current + timedelta(days=days)
    else:
        new_date = datetime.now() + timedelta(days=days)
    
    conn.execute(
        "UPDATE users SET premium_until = ? WHERE user_id = ?",
        (new_date.isoformat(), user_id)
    )
    conn.commit()
    conn.close()
    return new_date

def update_pomodoro_stats(user_id, cycles=1):
    conn = get_db()
    conn.execute(
        "UPDATE users SET pomodoro_cycles = pomodoro_cycles + ?, total_pomodoro_minutes = total_pomodoro_minutes + ? WHERE user_id = ?",
        (cycles, cycles * 25, user_id)
    )
    conn.commit()
    conn.close()