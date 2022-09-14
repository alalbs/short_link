from db import connection, cursor
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List
import hashlib
import uvicorn
import argparse
from psycopg2 import Error


# Парсер для обработки флага при запуске
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", action='store_true')
args = parser.parse_args()

# Используем FastAPI для создания API
app = FastAPI()

# Словарь для хранения ссылок, если при запуске не указан флаг -d
url_db = {}
_url = "http://localhost:8000/"


class URL(BaseModel):
    url: str

# Функция для обработки GET запросов
@app.get('/{hash}')
async def get_url(hash):
    try:
        # Если при запуске указан флаг -d, то обращаемся к базе данных
        if args.database:
            connection.commit()
            cursor.execute(f"SELECT URL from url WHERE HASH = '{hash}'")
            record = cursor.fetchone()
            return Response(headers={'Location': record[0]}, status_code=302)
        else:
            # Иначе обращаемся к словарю
            # Перенаправляем на нужную страницу с помощью header Location
            return Response(headers={'Location': url_db[hash]}, status_code=302) 
    except:
        return None

# Функция для обработки POST запросов
@app.post('/', status_code=201)
async def add_url(payload: URL):
    url = payload.dict()
    # Хешируем url с помощью sha256 и берем первые 6 символов
    hash = hashlib.sha256(url["url"].encode()).hexdigest()[:6]
    # Если при запуске указан флаг -d, то обращаемся к базе данных
    if args.database:
        try:
            connection.commit()
            insert_query = f""" INSERT INTO url (HASH, URL) VALUES ('{hash}', '{url["url"]}')"""
            cursor.execute(insert_query)
            connection.commit()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)    
    else:
        url_db[hash] = url["url"]
    return _url+hash

# Запускаем ASGI сервер
if __name__ == "__main__":
    uvicorn.run("shorturl:app", port=8000, log_level="info")

