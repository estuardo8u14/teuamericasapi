from ast import Str
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel, EmailStr, BaseModel
import uuid
from datetime import datetime
from typing import Union, List

#email imports
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

""" class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME = "username",
    MAIL_PASSWORD = "Pancho14!8!@",
    MAIL_FROM = "estuardo8u14@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "mail server",
    MAIL_FROM_NAME="TEUAmericas",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
) """


app = FastAPI()

origins = [
    "https://teu-americas-logistics.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    #expose_headers = ["*"],
)

class Item(BaseModel):
    nombre: str
    correo: str
    asunto: str
    mensaje: str


@app.get("/")
async def root():
    return {"message": "Enviado"}

#guardar en base de datos
@app.post("/post_contacto", response_model=Item)
def post_contacto(item:Item):
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5580269",
        password="fi5NuGf3Ha",
        database="sql5580269"
    )
    print(type(item))

    mycursor = mydb.cursor()

    sql = "INSERT INTO "+ "teuweb" +" (nombre, correo, asunto, mensaje) VALUES (%s, %s, %s, %s)"
    val = (
        item.nombre,
        item.correo,
        item.asunto,
        item.mensaje
    )
    mycursor.execute(sql, (val))
    mydb.commit()

    if(int(mycursor.rowcount) > 0):
        return True
    
    else:
        return False

#sacar de  base de datos
@app.get("/get_contacto")
def get_contacto(id : str):
    mydb = mysql.connector.connect(
        host="sql5.freesqldatabase.com",
        user="sql5580269",
        password="fi5NuGf3Ha",
        database="sql5580269"
    )
    mycursor = mydb.cursor()

    sql = "SELECT * FROM teuweb where id="+ id +""
    
    mycursor.execute(sql)
    results = mycursor.fetchall()

    
    data = []
    
    print(results) 


#Correo
""" @app.post("/email")
async def enviar_correo(email: EmailSchema) -> JSONResponse:
    html = """"""<p>Potencial Cliente:</p> <span>Nombre: {{ nombre }}!</span> """ """"

    message = MessageSchema(
        subject="Potencial Cliente",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"}) """
