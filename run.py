import os
import sqlite3
from flask import Flask
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用程式
# 指定 template_folder 與 static_folder 指向 app 資料夾之下
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-secret-key')

# 確保 instance 目錄存在
os.makedirs('instance', exist_ok=True)

# 註冊 Blueprints
from app.routes.main import main_bp
from app.routes.book import book_bp
from app.routes.review import review_bp

app.register_blueprint(main_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)

def init_db():
    """初始化資料庫的輔助函式，根據 database/schema.sql 建表"""
    database_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    if os.path.exists(schema_path):
        conn = sqlite3.connect(database_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully at instance/database.db.")
    else:
        print("Schema file not found! Please check database/schema.sql")

if __name__ == '__main__':
    app.run(debug=True)
