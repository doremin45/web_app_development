from flask import Blueprint, render_template

from app.models.book import get_all_books
from app.models.review import get_all_purchase_requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    處理首頁請求，顯示整體評分最高或最多人評論的熱門書籍排行。
    :return: 渲染並回傳 home.html
    """
    books = get_all_books()
    # 這裡可以直接將全庫書籍傳入，在 home.html 或透過 python 的 sorted 篩選前 N 名
    # 例如：依據 avg_rating 與 review_count 來排序做首頁焦點
    top_books = sorted(books, key=lambda x: (x.get('avg_rating', 0), x.get('review_count', 0)), reverse=True)[:10]
    return render_template('home.html', top_books=top_books)

@main_bp.route('/admin/reports', methods=['GET'])
def admin_reports():
    """
    處理館員專屬報表請求，統整需補貨或被讀者強烈推薦採購的清單。
    :return: 渲染並回傳 admin/reports.html
    """
    requests = get_all_purchase_requests()
    books = get_all_books()
    # 簡單篩選出庫存低於 3 的書當作補貨提醒清單
    low_inventory_books = [b for b in books if int(b['inventory']) < 3]
    return render_template('admin/reports.html', requests=requests, low_inventory_books=low_inventory_books)
