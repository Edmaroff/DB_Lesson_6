import sqlalchemy as sq
import json
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    def __str__(self):
        return (f'Название книги: {self.title}\n'
                f'ID издательства: {self.id_publisher}\n---------------')


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    books = relationship(Book, backref='publisher')

    def __str__(self):
        return (f'ID издательства: {self.id}\n'
                f'Название издательства: {self.name}\n'
                f'----------------------------')

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    def __str__(self):
        return (f'ID магазина: {self.id}\n'
                f'Название магазина: {self.name}\n'
                f'----------------------------')


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    books_stock = relationship(Book, backref='stock_books')
    shops_stock = relationship(Shop, backref='stock_shops')

    sq.CheckConstraint('count < 40', name='check_count_stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.DateTime)
    count = sq.Column(sq.Integer)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stock_sales = relationship(Stock, backref='sales_stock')

    sq.CheckConstraint('count < 100', name='check_count_sale')


# Удаление таблиц
def drop_tables(ses, engine):
    Base.metadata.drop_all(engine)
    ses.commit()
    return print('Таблицы удалены')

# Создание таблиц
def create_tables(ses, engine):
    Base.metadata.create_all(engine)
    ses.commit()
    return print('Таблицы созданы')

# Заполнение таблиц данными
def insert_table(ses, path):
  with open(path) as f:
    json_data = json.load(f)
  models = {
    'publisher': Publisher,
    'book': Book,
    'shop': Shop,
    'stock': Stock,
    'sale': Sale
  }
  for line in json_data:
    model = models.get(line.get('model'))
    ses.add(model(id=line.get('pk'), **line.get('fields')))
  ses.commit()
  return print('Таблицы заполнены')

# Поиск магазина по названию или id издателя
def search_shop(ses):
  publ_name = None
  publ_id = None
  publ = input('Введите название издательства или его идентификатор: ')
  if publ.isdigit():
    publ_id = publ
  else:
    publ_name = publ
  print(f'\nИздательство продается в магазинах:')
  for i in ses.query(Shop).join(Stock).join(Book).join(Publisher).\
          filter((Publisher.name == publ_name) | (Publisher.id == publ_id)).all():
    print(i)






































