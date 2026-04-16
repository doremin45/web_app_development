import sqlite3
import os
from datetime import datetime

# 根據專案結構，instance 目錄應該在 app.py 同層目錄
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_book(title, author, inventory=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO books (title, author, inventory, created_at) VALUES (?, ?, ?, ?)',
        (title, author, inventory, created_at)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id

def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, COALESCE(AVG(r.rating), 0) as avg_rating, COUNT(r.id) as review_count
        FROM books b
        LEFT JOIN reviews r ON b.id = r.book_id
        GROUP BY b.id
        ORDER BY b.created_at DESC
    ''')
    books = cursor.fetchall()
    conn.close()
    return [dict(book) for book in books]

def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, COALESCE(AVG(r.rating), 0) as avg_rating, COUNT(r.id) as review_count
        FROM books b
        LEFT JOIN reviews r ON b.id = r.book_id
        WHERE b.id = ?
        GROUP BY b.id
    ''', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return dict(book) if book else None

def update_book_inventory(book_id, inventory):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET inventory = ? WHERE id = ?', (inventory, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
