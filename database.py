#import mysql.connector
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, EmailStr
from typing import List
from mysql.connector import Error

host=os.getenv('RDS_HOST')
port=os.getenv('RDS_PORT')
user=os.getenv('RDS_USER')
password=os.getenv('RDS_PASSWORD')
database=os.getenv('RDS_DATABASE')


def connect_to_rds(database:str):
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database)
        status="Successfull"    
        return conn
    except mysql.connector.Error as err:
        status="Falied"
        return conn,status

def connect_to_localDB(database:str):
    conn=sqlite3.connect("user.db")
    cursor=conn.cursor()
    return cursor,conn



class UserFetchFormat(BaseModel):
    name: str
    phone_number: str
    address: str
    pincode: str
    email_id: EmailStr
    city: str
  









