import sqlite3
import hashlib
from datetime import datetime
import os

class Database:
    def __init__(self):
        try:
            # Get the current directory
            current_dir = os.getcwd()
            self.db_path = os.path.join(current_dir, 'chat_app.db')
            
            # Create database connection with explicit path
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print(f"Database connected successfully at: {self.db_path}")
            self._create_tables()
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            raise
    
    def _create_tables(self):
        try:
            # Create users table if it doesn't exist
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT NULL
            )
            ''')
            
            # Check if last_login column exists, if not add it
            self.cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in self.cursor.fetchall()]
            if 'last_login' not in columns:
                self.cursor.execute('ALTER TABLE users ADD COLUMN last_login TIMESTAMP DEFAULT NULL')
            
            # Create chat_history table if it doesn't exist
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')
            
            # Create user_state table if it doesn't exist
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_state (
                user_id INTEGER PRIMARY KEY,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_data TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            ''')
            
            self.conn.commit()
            print("Database tables verified successfully")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            raise
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        try:
            hashed_password = self._hash_password(password)
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error registering user: {str(e)}")
            return False
    
    def verify_user(self, username, password):
        try:
            hashed_password = self._hash_password(password)
            # First check if user exists and get their credentials
            self.cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
            result = self.cursor.fetchone()
            
            if result and result[1] == hashed_password:
                user_id = result[0]
                # Update last login time
                try:
                    self.cursor.execute(
                        'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
                        (user_id,)
                    )
                    self.conn.commit()
                except Exception as e:
                    print(f"Warning: Could not update last_login: {str(e)}")
                    # Don't rollback here, just continue
                
                return user_id
            return None
        except Exception as e:
            print(f"Error verifying user: {str(e)}")
            return None
    
    def save_chat_message(self, user_id, role, message):
        try:
            self.cursor.execute('INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)',
                         (user_id, role, message))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving chat message: {str(e)}")
            return False
    
    def get_chat_history(self, user_id):
        try:
            self.cursor.execute('SELECT role, message, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp',
                         (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching chat history: {str(e)}")
            return []
    
    def save_user_state(self, user_id, username, messages):
        try:
            # Update user's last activity
            self.cursor.execute(
                """
                INSERT INTO user_state (user_id, last_activity, session_data)
                VALUES (?, CURRENT_TIMESTAMP, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    last_activity = CURRENT_TIMESTAMP,
                    session_data = excluded.session_data
                """,
                (user_id, str(messages))
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving user state: {str(e)}")
            return False
    
    def get_user_state(self, user_id):
        try:
            self.cursor.execute('SELECT session_data FROM user_state WHERE user_id = ?',
                         (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching user state: {str(e)}")
            return None
    
    def __del__(self):
        try:
            self.conn.close()
        except:
            pass 