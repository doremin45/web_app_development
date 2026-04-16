from flask import Blueprint

book_bp = Blueprint('book', __name__, url_prefix='/books')

@book_bp.route('', methods=['GET'])
def list_books():
    """
    處理查詢或顯示系統內書籍列表，可包含搜尋參數過濾。
    :return: 渲染並回傳 books.html
    """
    pass

@book_bp.route('/new', methods=['GET'])
def new_book_form():
    """
    顯示新增書籍資料的表單頁面，供館員建檔使用。
    :return: 渲染並回傳 new_book.html
    """
    pass

@book_bp.route('', methods=['POST'])
def create_book():
    """
    接收新增書籍資料的表單並儲存至資料庫。
    :return: 成功後重導向至 books 清單或詳情頁，失敗則回傳 400
    """
    pass

@book_bp.route('/<int:book_id>', methods=['GET'])
def book_details(book_id):
    """
    根據書本 ID，顯示該書籍詳細資訊、目前庫存與所有網友心得評論紀錄。
    :param book_id: 書籍的唯一識別碼
    :return: 渲染並回傳 details.html，若書籍不存在回傳 404
    """
    pass

@book_bp.route('/<int:book_id>/inventory', methods=['POST'])
def update_inventory(book_id):
    """
    處理館員更新現有書籍庫存的請求。
    :param book_id: 書籍的唯一識別碼
    :return: 完成庫存更新後重導向回原書籍的詳情頁或清單
    """
    pass
