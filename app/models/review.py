import sqlite3
import os
from datetime import datetime

# 根據專案結構，instance 目錄應該在 app.py 同層目錄
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_review(book_id, content, rating):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO reviews (book_id, content, rating, created_at) VALUES (?, ?, ?, ?)',
        (book_id, content, rating, created_at)
    )
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()
    return review_id

def get_reviews_by_book_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE book_id = ? ORDER BY created_at DESC', (book_id,))
    reviews = cursor.fetchall()
    conn.close()
    return [dict(review) for review in reviews]

def add_purchase_request(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute(
        'INSERT INTO purchase_requests (book_id, created_at) VALUES (?, ?)',
        (book_id, created_at)
    )
    conn.commit()
    request_id = cursor.lastrowid
    conn.close()
    return request_id

def get_all_purchase_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pr.book_id, b.title, COUNT(pr.id) as request_count
        FROM purchase_requests pr
        JOIN books b ON pr.book_id = b.id
        GROUP BY pr.book_id
        ORDER BY request_count DESC
    ''')
    requests = cursor.fetchall()
    conn.close()
    return [dict(req) for req in requests]
