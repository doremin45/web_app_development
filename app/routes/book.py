from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.book import create_book, get_all_books, get_book_by_id, update_book_inventory
from app.models.review import get_reviews_by_book_id

book_bp = Blueprint('book', __name__, url_prefix='/books')

@book_bp.route('', methods=['GET'])
def list_books():
    """
    處理查詢或顯示系統內書籍列表，可包含搜尋參數過濾。
    """
    q = request.args.get('q', '').strip()
    books = get_all_books()
    
    if q:
        books = [b for b in books if q.lower() in b['title'].lower() or (b['author'] and q.lower() in b['author'].lower())]
        
    return render_template('books.html', books=books, q=q)

@book_bp.route('/new', methods=['GET'])
def new_book_form():
    """
    顯示新增書籍資料的表單頁面，供館員建檔使用。
    """
    return render_template('new_book.html')

@book_bp.route('', methods=['POST'])
def create_book_action():
    """
    接收新增書籍資料的表單並儲存至資料庫。
    """
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    inventory_str = request.form.get('inventory', '0').strip()
    
    # 驗證必填
    if not title:
        flash('登錄失敗：書名為必填欄位', 'danger')
        return render_template('new_book.html', title=title, author=author, inventory=inventory_str)
        
    # 驗證庫存數字
    try:
        inventory = int(inventory_str)
        if inventory < 0:
            raise ValueError
    except ValueError:
        flash('登錄失敗：庫存數量必須是大於或等於零的整數', 'danger')
        return render_template('new_book.html', title=title, author=author, inventory=inventory_str)
        
    book_id = create_book(title, author, inventory)
    if book_id is None:
        flash('系統發生錯誤，無法寫入資料庫', 'danger')
        return render_template('new_book.html', title=title, author=author, inventory=inventory_str)
        
    flash('書籍新增成功！', 'success')
    return redirect(url_for('book.list_books'))

@book_bp.route('/<int:book_id>', methods=['GET'])
def book_details(book_id):
    """
    根據書本 ID，顯示該書籍詳細資訊、目前庫存與所有網友心得評論紀錄。
    """
    book = get_book_by_id(book_id)
    if not book:
        flash('找不到該本圖書', 'warning')
        return redirect(url_for('book.list_books'))
        
    reviews = get_reviews_by_book_id(book_id)
    return render_template('details.html', book=book, reviews=reviews)

@book_bp.route('/<int:book_id>/inventory', methods=['POST'])
def update_inventory(book_id):
    """
    處理館員更新現有書籍庫存的請求。
    """
    # 確認書本存在
    if not get_book_by_id(book_id):
        flash('存取被拒，找不到該書籍', 'danger')
        return redirect(url_for('book.list_books'))

    inventory_str = request.form.get('inventory', '').strip()
    try:
        inventory = int(inventory_str)
        if inventory < 0:
            raise ValueError
    except ValueError:
        flash('錯誤：更新的庫存量必須是大於或等於零的數字。', 'danger')
        return redirect(url_for('book.book_details', book_id=book_id))
        
    success = update_book_inventory(book_id, inventory)
    if success:
        flash('庫存數量更新成功！', 'success')
    else:
        flash('資料庫更新發生錯誤，請稍後再試。', 'danger')
        
    return redirect(url_for('book.book_details', book_id=book_id))
