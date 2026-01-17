import sqlite3
import random

def init_db():   #init data base 
    try:
        conn = sqlite3.connect("secure_access.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                zone_level INTEGER,
                pin_code TEXT,
                biometric_hash TEXT,
                scan_count INTEGER,
                last_x INTEGER DEFAULT 7
            )
        ''')
        conn.commit()
    except Exception as e:
        print("[ERROR] init_db failed:", e)
    finally:
        conn.close()


class User:    #init user
    def __init__(self, user_id, name, zone_level, pin_code, biometric_hash="", scan_count=0, last_x=None):
        self.user_id = user_id
        self.name = name
        self.zone_level = zone_level
        self.pin_code = pin_code
        self.biometric_hash = biometric_hash
        self.scan_count = scan_count
        self.last_x = last_x if last_x is not None else random.randint(5, 15)

    def save_to_db(self):  # Save the user into the database
        conn = sqlite3.connect("secure_access.db")
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO users
            (user_id, name, zone_level, pin_code, biometric_hash, scan_count, last_x)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, self.name, self.zone_level, self.pin_code,
              self.biometric_hash, self.scan_count, self.last_x))
        conn.commit()
        conn.close()

    @staticmethod   # Load a user from the database by id
    def load_from_db(user_id):
        conn = sqlite3.connect("secure_access.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = c.fetchone()
        conn.close()
        if row:
            try:
                return User(*row)
            except TypeError as e:
                print(f"[ERROR] Failed to load User with row={row}")
                print(f"[DETAILS] {e}")
        return None

    def delete_from_db(self): # Delete user from the database
        conn = sqlite3.connect("secure_access.db")
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE user_id=?", (self.user_id,))
        conn.commit()
        conn.close()

