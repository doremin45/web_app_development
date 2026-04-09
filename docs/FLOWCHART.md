# 讀書筆記本系統 - 流程圖設計

本文件根據 PRD 與系統架構設計（ARCHITECTURE），定義了「讀書筆記本系統」的使用者操作路徑（User Flow）、系統序列圖（Sequence Diagram）以及詳細的功能與 API 對應清單，確保後續實作階段能夠清楚了解資料流動與使用者體驗。

## 1. 使用者流程圖（User Flow）

此流程圖描述了「讀者」與「圖書人員」在系統內主要的瀏覽步驟與操作路徑。

```mermaid
flowchart LR
    Start([開始開啟網頁]) --> Home[首頁 - 瀏覽熱門書籍排行榜]
    
    Home -->|點擊瀏覽或搜尋| Books[書籍清單/搜尋結果頁面]
    Books --> ViewBook[進入單一書籍詳情頁面]
    
    ViewBook --> ReaderAction{讀者操作選項}
    ReaderAction -->|撰寫心得/星級評分| AddReview[填寫讀書心得表單]
    ReaderAction -->|推薦圖書館採購| Recommend[點擊提出進書推薦]
    
    AddReview --> ViewBook
    Recommend --> ViewBook
    
    Home -->|館員登入後台| Admin[館員管理介面]
    Admin --> AdminAction{圖書人員管理操作}
    AdminAction -->|書籍建檔| AddBook[填寫新增書籍表單]
    AdminAction -->|進出庫管理| Inventory[更新書籍庫存數]
    AdminAction -->|盤點與採購需求| ReviewReports[查看讀者高評分與二度購買需求清單]
    
    AddBook --> Admin
    Inventory --> Admin
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖描述核心功能：「從讀者在書籍詳情頁準備提交讀書心得與評分，到資料庫成功儲存並重新渲染畫面」的完整系統資料流。

```mermaid
sequenceDiagram
    actor User as 讀者
    participant Browser as 瀏覽器
    participant Flask as Flask (review.py)
    participant Model as Model (review)
    participant DB as SQLite database.db
    
    User->>Browser: 填寫心得內容並選擇 1~5 星評分，點擊送出
    Browser->>Flask: POST /books/<id>/reviews (夾帶表單資料)
    Flask->>Model: 呼叫 add_review(book_id, content, rating)
    Model->>DB: INSERT INTO reviews (book_id, content, rating...)
    DB-->>Model: 回傳寫入成功
    Model-->>Flask: 成功處理完成
    Flask-->>Browser: HTTP 302 重導向回 /books/<id> 頁面
    Browser->>Flask: GET /books/<id> (重新取得最新資料)
    Flask-->>Browser: 回渲染完畢的 Jinja2 HTML 畫面
    Browser-->>User: 畫面更新，顯示剛提交的心得與最新平均評分
```

## 3. 功能清單對照表

下表列出系統所有核心功能其對應的 URL 路徑、HTTP 方法與負責處理該請求的 Router。

| 功能名稱 | URL 路徑 (範例) | HTTP 方法 | 對應 Route | 描述 |
| ------ | ------------- | -------- | --------- | ---- |
| **首頁 (排行榜)** | `/` | GET | `main.py` | 顯示全站評價最高或最受歡迎（最多人評論）的書籍列表 |
| **書籍清單/搜尋** | `/books` | GET | `book.py` | 列出系統內書籍，並可依書名、作者進行查詢 |
| **單一書籍詳情** | `/books/<id>` | GET | `book.py` | 顯示書籍詳細資訊、歷史評論、平均評分與當前庫存 |
| **新增書籍 (建檔)** | `/books/new` | GET, POST | `book.py` | 館員進入建檔表單，並透過 POST 接收資料存入庫 |
| **更新書籍庫存** | `/books/<id>/inventory` | POST | `book.py` | 圖書人員透過表單或按鈕快速更新該書籍庫存數量 |
| **新增讀書心得/評分** | `/books/<id>/reviews` | POST | `review.py` | 讀者提交特定書籍的文字心得與 1~5 星評級 |
| **提出進書推薦/補貨需求** | `/books/<id>/recommend` | POST | `review.py` | 讀者針對缺貨或喜愛的原書點選按鈕，紀錄「二度購買需求」 |
| **館員採購/熱門清單** | `/admin/reports` | GET | `main.py` / `book.py`| 圖書館員專屬頁面，統整需補貨、被推薦採購或高評分的清單 |
