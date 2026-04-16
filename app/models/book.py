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

def create_book(title, author, inventory=0):
    """
    新增一筆書籍記錄。
    :param title(str): 書名
    :param author(str): 作者
    :param inventory(int): 庫存數量
    :return(int): 新增的書籍 id，失敗為 None
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO books (title, author, inventory, created_at) VALUES (?, ?, ?, ?)',
            (title, author, inventory, created_at)
        )
        conn.commit()
        book_id = cursor.lastrowid
        return book_id
    except sqlite3.Error as e:
        print(f"Error creating book: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_all_books():
    """
    取得所有書籍記錄，並關聯計算平均評分與評論數。
    :return(list): 包含字典的書籍列表
    """
    try:
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
        return [dict(book) for book in books]
    except sqlite3.Error as e:
        print(f"Error getting all books: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_book_by_id(book_id):
    """
    取得單筆書籍記錄及其評分狀態。
    :param book_id(int): 書籍 ID
    :return(dict/None): 書籍資料字典，找不到時回傳 None
    """
    try:
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
        return dict(book) if book and book['id'] is not None else None
    except sqlite3.Error as e:
        print(f"Error getting book by id: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def update_book_inventory(book_id, inventory):
    """
    更新書籍的庫存數量。
    :param book_id(int): 書籍 ID
    :param inventory(int): 新的庫存數量
    :return(bool): 成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE books SET inventory = ? WHERE id = ?', (inventory, book_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating book inventory: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def delete_book(book_id):
    """
    刪除指定的書籍（包含關聯的心得會透過 CASCADE 刪除）。
    :param book_id(int): 書籍 ID
    :return(bool): 成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting book: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()
