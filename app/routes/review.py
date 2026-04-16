from flask import Blueprint

review_bp = Blueprint('review', __name__, url_prefix='/books/<int:book_id>')

@review_bp.route('/reviews', methods=['POST'])
def add_review(book_id):
    """
    接受從詳情頁表單送出的讀者心得內容與星級評分（1~5星）。
    :param book_id: 關聯的書籍 ID
    :return: 將評論存入資料庫後重導向回原本的書籍詳情頁
    """
    pass

@review_bp.route('/recommend', methods=['POST'])
def add_recommendation(book_id):
    """
    當讀者點擊「推薦購買／提醒補貨」時觸發，紀錄一筆二度購買的需求資料。
    :param book_id: 關聯的書籍 ID
    :return: 儲存請求後重導向回原本的書籍詳情頁
    """
    pass
