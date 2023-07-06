import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="dataBase"
)

df = pd.read_csv('filename.csv')