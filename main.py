from fastapi import FastAPI, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


app = FastAPI(
    title= "Logging API",
    description = "An API for all logging needs.",
    version = "2.0"
    )

# declare body
class Item(BaseModel):
    name:str
    price: float
    is_offer: Optional[bool] = None

# Each operation is an requests executed by the easy API

@app.get("/")  # take GET operation
async def main():
    content="""
    <body>
    <form action = "/files/" enctype="multipart/form-data" method = "post">
    <input name = "files" type="file" multiple>
    <input type = "submit">
    </form>
    </body>
    """
    
    return HTMLResponse(content=content)

@app.get("/items/{item_id}")
def read_item(item_id:int, q: Optional[str] = None):
    return {"item_id":item_id, "q":q}

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    return {"item_name": item.name, "item_price":item.price}

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size":len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename":file.filename}



#if __name__ == '__main__':
    