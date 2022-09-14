
import configparser
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


config = configparser.ConfigParser()
config.read('config.ini')



try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user=f'{config["DATABASE"]["User"]}',
                                  # пароль, который указали при установке PostgreSQL
                                  password=f'{config["DATABASE"]["Password"]}',
                                  host="127.0.0.1",
                                  port="5432")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE url_db')
        connection.commit()
        cursor.close()
        connection.close()
    except psycopg2.ProgrammingError as e:
        print("Already exists")
    try:
        connection = psycopg2.connect(user=f'{config["DATABASE"]["User"]}',
                                  # пароль, который указали при установке PostgreSQL
                                  password=f'{config["DATABASE"]["Password"]}',
                                  host="127.0.0.1",
                                  port="5432",
                                  database="url_db")
        create_table_query = '''CREATE TABLE url
                          (HASH VARCHAR PRIMARY KEY     NOT NULL,
                          URL           VARCHAR    NOT NULL); '''
        # Выполнение команды: это создает новую таблицу
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица успешно создана в PostgreSQL")
    except psycopg2.ProgrammingError as e:
        print("Already exists")
        
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
