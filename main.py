import configparser
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from modeles import create_tables, drop_tables, insert_table, search_shop, Book, Publisher, Shop, Stock, Sale
from dotenv import load_dotenv


if __name__ == '__main__':
    # # Переменные для создания подключения (1 вариант)
    # config = configparser.ConfigParser()
    # config.read("settings.ini")
    # connection_driver = config['SQL']['connection_driver']
    # username = config['SQL']['username']
    # password = config['SQL']['password']
    # server_name = config['SQL']['server_name']
    # port = config['SQL']['port']
    # db_name = config['SQL']['db_name']
    #
    # Переменные для создания подключения (2 вариант - переменные окружения)
    load_dotenv()
    connection_driver = os.getenv('connection_driver')
    username = os.getenv('user')
    password = os.getenv('password')
    server_name = os.getenv('server_name')
    port = os.getenv('port')
    db_name = os.getenv('db_name')
    #
    # Создание подключения
    DSN = f'{connection_driver}://{username}:{password}@{server_name}:{port}/{db_name}'
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Проверка удаления и создания таблиц
    drop_tables(session, engine)
    create_tables(session, engine)

    # Проверка заполнения таблиц
    BASE_DIR = os.getcwd()
    FOLDER_NAME = 'fixtures'
    FILE_NAME = 'tests_data.json'
    full_path = os.path.join(BASE_DIR, FOLDER_NAME, FILE_NAME)
    insert_table(session, full_path)

    # Проверка поиска магазина по названию или id издателя
    search_shop(session)
    session.close()
