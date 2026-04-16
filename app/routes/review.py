from flask import Blueprint, request, redirect, url_for, flash
from app.models.review import add_review, add_purchase_request
from app.models.book import get_book_by_id

review_bp = Blueprint('review', __name__, url_prefix='/books/<int:book_id>')

@review_bp.route('/reviews', methods=['POST'])
def add_review_action(book_id):
    """
    接受從詳情頁表單送出的讀者心得內容與星級評分（1~5星）。
    """
    content = request.form.get('content', '').strip()
    rating_str = request.form.get('rating', '').strip()
    
    if not content or not rating_str:
        flash('無法送出評論：心得內容與評分皆為必填項目。', 'danger')
        return redirect(url_for('book.book_details', book_id=book_id))
        
    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        flash('操作失敗：評分必須為 1 到 5 之間的整數。', 'danger')
        return redirect(url_for('book.book_details', book_id=book_id))
        
    review_id = add_review(book_id, content, rating)
    if review_id:
        flash('心得送出成功！感謝您的分享！', 'success')
    else:
        flash('系統忙碌中，心得存取失敗。', 'danger')
        
    return redirect(url_for('book.book_details', book_id=book_id))

@review_bp.route('/recommend', methods=['POST'])
def add_recommendation(book_id):
    """
    當讀者點擊「推薦購買／提醒補貨」時觸發，紀錄一筆二度購買的需求資料。
    """
    book = get_book_by_id(book_id)
    if not book:
        flash('找不到指定書籍，操作無效。', 'danger')
        return redirect(url_for('main.index'))
        
    request_id = add_purchase_request(book_id)
    if request_id:
        flash(f'成功為《{book["title"]}》提交了一筆補貨/推薦需求！圖書館將列入考量。', 'success')
    else:
        flash('系統異常，您的推薦需求未能成功記錄。', 'danger')
        
    return redirect(url_for('book.book_details', book_id=book_id))
