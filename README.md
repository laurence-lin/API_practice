# API_practice
Practice to build an API server and write an RESTful API for web &amp; APP service

Written with python FastAPI:
Build local API server and simple RESTful API


API 筆記:
RESTful API: 一種API 設計標準

使用 HTTP protocal (GET/POST/PUT/DELETE) 來實現 API 所需要的各種功能, 使設計時風格統一化

 
HTTP method:
GET: 取得資料
POST: 新增資料, 若已存在則新增
PUT: 更新資料, 若已存在則覆蓋
DELETE: 刪除資料

RESTful API 特徵:
1.	善用 http verb
2.	直觀的資源URL
3.	操作資料類行為Web可接受: json, xml, yaml等

同步與非同步:
同步: 工作一做完後, 在開始進行工作二

非同步: 工作一做到一半, 資源還有閒置時先開始進行工作二, 最後整體而言所有工作完成時間縮短, 達到省時間的目的, 有效利用閒置資源.

API 測試站:
Swagger UI: 可測試 API 的各個 requests 效果, 輸入不同的值

Command line 呼叫 API:
Curl: 在 OS 上用來和 HTTP protocol 下載上傳檔案的指令, 比wget只能下載通能更多. 可用 curl 發送 API request: curl –X GET “requests url”

在 python 中對網頁伺服器提出 API 請求: 使用 requests 模組對 web server 呼叫要求
如: GET 要求
R = requests.get(‘http://localhost:8000/items/5?account=8’)
Print(R.text)

使用 api 發送請求, 目標 web server 須保持開啟可連線狀態.

Note 注意事項: The data transformed by API might involves security issue. There are multiple ways to hack and attach the data within API by others that aren't permitted.

Python API framework: 

Flask: 可建立網頁Server 和 API, 以micro概念為基礎設計的framework
  A micro web application development tools: 'micro' means Flask is small basic but extensible. We could extend Flask with database integration, upload handling... and so on.
  If may not include all aspects of function, but extensible by ourself when needed.
  
Run Flask APP:
  After finished a .py file holds the APP: 
     1. Tell terminal which APP to work with by exportking FLASK_APP environment variable: 
          In CMD: export FLASK_APP = my_file.py
  
     2. Run with flask command: in CMD: flask run, or in Python: python -m flask run

Externally visible server: Originally, the server built only run on the builder's computer, this is due to the debug mode.
    Now if a user in same network on another computer want access to this server, setup the host IP by: flask run --host=0.0.0.0 <= tells the OS to listen on all IPs
    
Debug mode: 
   Originally development mode, every change of our code we have to restart the code. Enabling debug support then the code changes might update itself to help debug.
   Set development features: export FLASK_ENV environment variable to development:
     export FLASK_ENV=development
     flask run
     
Render the HTML file content:
   1. Create template folder behind main code.py file named "templates":
      app.py
      templates
         -file.html
         
   2. Then use render_templateset FLA

                           
  
  
  
  
  
  
  
  
  
  
  








