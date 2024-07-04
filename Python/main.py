from pymongo import MongoClient
from fastapi import FastAPI, Request, Form, File, UploadFile
from starlette.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.templating import Jinja2Templates
from PIL import Image
import tensorflow as tf
import numpy as np
import io
from dotenv import load_dotenv
import os
# from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
db_pass = os.getenv("DB_PASS")

db_connection_string = f"mongodb+srv://prishasawhney:{db_pass}@mycluster.bpqhvmj.mongodb.net/"
client=MongoClient(db_connection_string)
templates = Jinja2Templates(directory="HTML")

model = tf.keras.models.load_model(r'Models\Classify.h5')

app = FastAPI()
app.mount("/css", StaticFiles(directory=r"CSS"), name="css")
app.mount("/assets", StaticFiles(directory=r"Assets"), name="assets")
app.mount("/js", StaticFiles(directory=r"JS"), name="js")

# Adding cors urls
# origins = [
#     "http://localhost:3000",
#     ]

# Add middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )

# print("Initiating...")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/upload")
async def signup(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/signup")
async def newUser(request: Request, uname: str = Form(...) , email_id: str = Form(...), pswd: str = Form(...), pswd2: str = Form(...)):
    mydb = client["SampleWebsite"]
    mycol = mydb["users"]
    if(pswd!=pswd2):
        data = [1, 2, 3, 4, 5]
        msg = "The re-entered password does not match"
        return templates.TemplateResponse("signup.html",{"request" : request, "error" : msg, "data" : data})
    elif(mycol.count_documents({"username":uname})>0):
        msg = "This username is already taken"
        return templates.TemplateResponse("signup.html",{"request" : request, "error" : msg})
    else:
        rec = {"username": uname, "email" : email_id , "password" : pswd}
        x=mycol.insert_one(rec)
        msg = "Record inserted successfully"
        return templates.TemplateResponse("upload.html",{"request" : request, "response": "Logged in!"})

@app.post("/login")
async def oldUser(request: Request, uname: str = Form(...) , pswd: str = Form(...)):
    mydb = client["SampleWebsite"]
    mycol = mydb["users"]
    if(mycol.count_documents({"username":uname})==0):
        msg = "This username does not exist"
        return templates.TemplateResponse("login.html",{"request" : request, "error" : msg})
    else:
        rec = mycol.find({"username":uname})
        if (pswd != rec[0]["password"]):
            msg = "Incorrect password!"
            return templates.TemplateResponse("login.html",{"request" : request, "error" : msg})
        else:
            msg = "Successfully Logged in"
            return templates.TemplateResponse("upload.html",{"request" : request, "response": msg})

@app.post("/results/")
async def check_disease_level(request: Request,file: UploadFile = File(...)):
    # file: is the name given to input tag
    # type is file!!!!!!

    try:
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        img = Image.open(io.BytesIO(contents))
        img = img.resize((224,224))
        img_array = np.array(img)
        img_tensor = np.expand_dims(img_array,axis=0)

        preds = model.predict(img_tensor)
        predicted_class = np.argmax(preds)
        
        class_idx = np.argmax(preds[0])
        class_prob = preds[0][class_idx]
        class_labels = ['Mild', 'Moderate', 'Negative', 'Proliferated', 'Severe']
        disease_stage=class_labels[predicted_class]
        return JSONResponse(content={"disease_stage": disease_stage})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=5000, reload=True)

