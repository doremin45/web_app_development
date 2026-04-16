from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    處理首頁請求，顯示整體評分最高或最多人評論的熱門書籍排行。
    :return: 渲染並回傳 home.html
    """
    pass

@main_bp.route('/admin/reports', methods=['GET'])
def admin_reports():
    """
    處理館員專屬報表請求，統整需補貨或被讀者強烈推薦採購的清單。
    :return: 渲染並回傳 admin/reports.html
    """
    pass
