# -*- coding: utf-8 -*-

from fastapi import FastAPI, File, UploadFile
import spacy
from utils import *
from os import path
from datetime import datetime

app = FastAPI(
  title = "以文找文API",
  version= "v1.0 2021.05 HamastarAI",
  description = '''上傳檔案格式必須為二進制JSON，必須包含兩個欄位，SN為文本序號之整數值，text為文本內容之字串。例如：

  [{"SN": 123, "text":"文本一"},
   {"SN": 456, "text":"文本二"}]

  使用方法：
  1. /：檢查是否已有向量索引資料庫。 
  2. /test/：上傳測試文本，檢查文本欄位是否正確。
  3. /create/：上傳完整文本資料庫，建立向量索引。
  4. /search/：給定文本SN，回傳相似文本SN。topK為相似文本數量，預設值為10。
  5. /update/：新增文本，更新向量索引資料庫。
  ''',
)
nlp = spacy.load("zh_core_web_md")


# Connect to DB:
with open("db_setting.txt") as f:
        setting = f.readlines()

for content in setting:
        if "DB" in content:
            database = content.split("=")[1].strip()
        elif "user" in content:
            user = content.split("=")[1].strip()
        elif "host" in content:
            host = content.split("=")[1].strip()
        elif "port" in content:
            port = content.split("=")[1].strip()
        elif "password" in content:
            password = content.split("=")[1].strip()
            
import psycopg2

connector = psycopg2.connect(dbname = database,
                             user = user,
                             host = host,
                             port = port,
                             password = password)

print('Connect to DB successful!')


@app.get("/")
async def check_status():
  status = path.exists("index.bin")
  if status:
    message = "文本索引資料庫已建立完成，可開始查詢相似文本。"
  else:
    message = "找不到索引資料庫，請先建立資料庫!"
  return message 

@app.get("/results/")
async def display_result():
    
    query = """
       select * from public."AISP_feedback"
    """
    
    with connector.cursor() as curs:
        curs.execute(query)
        
        result = curs.fetchall()
    print(result)
        
    return result

@app.post("/feedback")
async def feedback(Input: list, Predict: list, feed: int):
    
    query = """
      INSERT INTO public."AISP_feedback"
        ("Input", "Prediction", "Feedback", "CreateDate")
      VALUES
        (Input, {}, {}, {})
    """.format(str(Predict[:]), str(feed), datetime.now())
    
    with connector.cursor() as curs:
        curs.execute(query)
    
    return "Feedback successed!"

@app.post("/test/")
async def upload_testdata(json_file: UploadFile = File(...)):
    contents = await json_file.read()
    df = pandas.read_json(contents)
    df = preprocess_df(df)
    message = f"已成功上傳{df.shape[0]}筆資料!"
    return message

@app.post("/create/")
async def upload_database(json_file: UploadFile = File(...)):
    contents = await json_file.read()
    df = pandas.read_json(contents)
    df = preprocess_df(df)
    text_list = df.text.to_list()
    SN_series = df.SN.values

    doc_vectors = []
    for doc in nlp.pipe(text_list, disable=["tagger", "parser", "ner"]):
      doc_vectors.append(doc.vector)

    index = create_index(doc_vectors, SN_series)
    message = f"已建立{index.ntotal}個文本的Faiss索引!"
    return message

@app.get("/search/")
async def find_similar(sn: int, topK: int = 10):
  status = path.exists("index.bin")
  if status:
    index = load_index()
    embeddings = load_embeddings()
    position = SN2position(index, sn)

    if position != None:
      D, I = index.search(np.array([embeddings[position]]), k=topK)
      SNs = I.flatten().tolist()
      return SNs
    else:
      message = "文本序號不在索引資料庫當中，請先新增至資料庫!"
      return message 
  
  else:
    message = "找不到索引資料庫，請先建立資料庫!"
    return message

@app.post("/update/")
async def update_index(json_file: UploadFile = File(...)):
  status = path.exists("index.bin")
  if status:
    index = load_index()
    old_embeddings = load_embeddings()

    contents = await json_file.read()
    df = pandas.read_json(contents)
    df = preprocess_df(df)
    text_list = df.text.to_list()
    new_doc_num = len(text_list)
    SN_series = df.SN.values

    doc_vectors = []
    for doc in nlp.pipe(text_list, disable=["tagger", "parser", "ner"]):
      doc_vectors.append(doc.vector)

    # Step 1: Change data type
    new_embeddings = np.array([embedding for embedding in doc_vectors]).astype("float32")
    # Step 2: Add new embeddings to the index
    index.add_with_ids(new_embeddings, SN_series)
    # Step 3: Combine the old and new embeddings
    combined_embeddings = np.concatenate((old_embeddings, new_embeddings))

    # Save the combined embeddings
    with open("embeddings.npy", "wb") as f:
      np.save(f, combined_embeddings)
    # Save the updated index
    faiss.write_index(index, "index.bin")

    message = f"已新增{new_doc_num}個文本的Faiss索引!"

  else:
    message = "找不到索引資料庫，請先建立資料庫!"
  
  return message
