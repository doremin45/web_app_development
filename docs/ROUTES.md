# 路由與頁面設計文件 (ROUTES)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| ---- | -------- | -------- | ------- | ---- |
| 首頁 (排行榜) | GET | `/` | `home.html` | 顯示全站評價最高或最受歡迎的書籍列表 |
| 館員報表 | GET | `/admin/reports` | `admin/reports.html` | 圖書館員專屬，統整需補貨、被推薦採購或高評分的清單 |
| 書籍清單/搜尋 | GET | `/books` | `books.html` | 列出系統內書籍，並可依書名、作者進行查詢 |
| 新增書籍表單 | GET | `/books/new` | `new_book.html` | 顯示新增書籍的表單畫面 |
| 建立書籍 (送出) | POST | `/books` | — | 接收新增書籍表單，存入 DB，完成後導回清單 |
| 單一書籍詳情 | GET | `/books/<int:id>` | `details.html` | 顯示書籍詳細資訊、歷史評論、平均評分與現有庫存 |
| 更新書籍庫存 | POST | `/books/<int:id>/inventory` | — | 更新庫存，完成後重導向回詳情頁 |
| 新增讀書心得 | POST | `/books/<int:id>/reviews` | — | 接受文字心得與 1~5 星評分，完成後重導向回詳情頁 |
| 提出進書推薦 | POST | `/books/<int:id>/recommend` | — | 針對缺貨或熱門書籍發出二度購買需求，完成後導回詳情頁 |

## 2. 每個路由的詳細說明

### main.py
- **`/` (GET)** 
  - **輸入:** 無
  - **邏輯:** 呼叫 Model 取得平均評分最高或評論數最多的書籍清單。
  - **輸出:** 渲染 `home.html`，傳遞書籍排行榜。
  - **錯誤處理:** 無資料時顯示預設訊息。

- **`/admin/reports` (GET)**
  - **輸入:** 無
  - **邏輯:** 呼叫 Model 提取庫存過低，或是收到最多次二度購買需求 (`purchase_requests`) 的標的書籍。
  - **輸出:** 渲染 `admin/reports.html` 給館員查看。

### book.py
- **`/books` (GET)**
  - **輸入:** URL Query 參數 (選填，如 `?q=關鍵字`)。
  - **邏輯:** 若有關鍵字，過濾對應的書籍，若無則列出所有書籍。
  - **輸出:** 渲染 `books.html`，傳遞包含搜尋結果的書籍列表。

- **`/books/new` (GET)**
  - **輸入:** 無
  - **邏輯:** 單純回傳新增頁面。
  - **輸出:** 渲染 `new_book.html` 供管理員使用。

- **`/books` (POST)**
  - **輸入:** 表單資料 (`title`, `author`, `inventory`)
  - **邏輯:** 呼叫 Model 的 `create_book`，並檢查 `title` 必填與庫存預設驗證。
  - **輸出:** 成功後 `redirect` 到書籍清單 (`/books`)。
  - **錯誤處理:** 資料不完整回傳 HTTP 400，或顯示錯誤訊息給前端。

- **`/books/<int:id>` (GET)**
  - **輸入:** 從 URL 取得之 `id`
  - **邏輯:** 透過 `id` 取得該書籍本身資訊、平均評分以及所有的評論 (`reviews`) 陣列資料。
  - **輸出:** 渲染 `details.html`。
  - **錯誤處理:** 書籍 `id` 不存在則回傳 404 Not Found。

- **`/books/<int:id>/inventory` (POST)**
  - **輸入:** 表單傳遞新庫存數量 (`inventory`)，以及 URL 傳遞的 `id`
  - **邏輯:** 呼叫 Model 覆寫新庫存資料至該筆書籍。
  - **輸出:** 成功後 `redirect` 到 `/books/<id>`。

### review.py
- **`/books/<int:id>/reviews` (POST)**
  - **輸入:** 表單取得 `content`, `rating`，並透過 URL 取得 `book_id`
  - **邏輯:** 呼叫 Model 新增心得與評分。檢查評分是否在 1-5 星範圍內。
  - **輸出:** 成功後 `redirect` 到 `/books/<id>`。
  - **錯誤處理:** 輸入若有惡意字眼可在此過濾防範，範圍不正確時阻擋寫入。

- **`/books/<int:id>/recommend` (POST)**
  - **輸入:** 從 URL 取得之 `book_id`
  - **邏輯:** 使用 Model 單次紀錄一筆需求 (`purchase_requests`)。
  - **輸出:** 成功後 `redirect` 到 `/books/<id>`，並可能回傳已接受建議的提示（Flash Messages）。

## 3. Jinja2 模板清單

我們將會準備下列所有前端模板：

- **`layout.html`**: 網站基礎佈局 (Base Template)，包含 Navigation 及共用 CSS/JS 引用。
- **`home.html`**: 此頁面呈現排行榜，繼承自 `layout.html`。
- **`books.html`**: 此頁面會列表顯示系統內所有書籍或者搜尋結果，繼承自 `layout.html`。
- **`new_book.html`**: 新增書目的表單視圖，繼承自 `layout.html`。
- **`details.html`**: 可顯示單一實體書籍，下方包含撰寫心得及顯示所有使用者留言的區塊，繼承自 `layout.html`。
- **`admin/reports.html`**: 管理員專用的採購資訊統整版面，繼承自 `layout.html`。

## 4. 路由骨架程式碼
具體宣告於下列檔案中：
- `app/routes/main.py`
- `app/routes/book.py`
- `app/routes/review.py`
