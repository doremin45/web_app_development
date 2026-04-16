import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """建立並取得 SQLite 資料庫連線，設定 row_factory。"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

def add_review(book_id, content, rating):
    """
    新增一筆書籍心得評價。
    :param book_id(int): 關聯的書籍 ID
    :param content(str): 心得內容
    :param rating(int): 評分 (1-5 星)
    :return(int/None): 新增的心得 id，失敗回傳 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO reviews (book_id, content, rating, created_at) VALUES (?, ?, ?, ?)',
            (book_id, content, rating, created_at)
        )
        conn.commit()
        review_id = cursor.lastrowid
        return review_id
    except sqlite3.Error as e:
        print(f"Error adding review: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_reviews_by_book_id(book_id):
    """
    根據書本 ID 取得所有心得評價記錄。
    :param book_id(int): 關聯的書籍 ID
    :return(list): 心得記錄列表
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews WHERE book_id = ? ORDER BY created_at DESC', (book_id,))
        reviews = cursor.fetchall()
        return [dict(review) for review in reviews]
    except sqlite3.Error as e:
        print(f"Error getting reviews per book: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def add_purchase_request(book_id):
    """
    新增一筆特定書籍的進書（二度購買）需求。
    :param book_id(int): 關聯的書籍 ID
    :return(int/None): 新增的需求 id，失敗回傳 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO purchase_requests (book_id, created_at) VALUES (?, ?)',
            (book_id, created_at)
        )
        conn.commit()
        request_id = cursor.lastrowid
        return request_id
    except sqlite3.Error as e:
        print(f"Error adding purchase request: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_all_purchase_requests():
    """
    取得所有被讀者提出進書需求的書籍清單，並依需求數排列。
    :return(list): 包含目標書名及其需求次數的列表
    """
    try:
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
        return [dict(req) for req in requests]
    except sqlite3.Error as e:
        print(f"Error getting purchase requests: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
