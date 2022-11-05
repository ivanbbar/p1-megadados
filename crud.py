import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, insert, delete, update, and_
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("USER")
password = os.getenv("PASSWORD")

engine = create_engine(f'mysql+pymysql://{username}:{password}@localhost/estoque')
db = automap_base()
db.prepare(engine, reflect=True)

def row2dict(row):
    # https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

def query2object(query):
    result = []
    for row in query:
        result.append(row2dict(row))
    return result

class CrudProducts():
    def __init__(self):
        self.session = Session(engine)
        self.Product = db.classes.product

    def create(self, object):
        with engine.connect() as conn:
            return conn.execute(insert(self.Product).values(name=object["name"], price=object["price"], description=object["description"]))

    def get_all(self):
        result = []
        for row in self.session.query(self.Product).all():
            result.append(row2dict(row))
        return result

    def get(self, product_id):
        result = []
        for row in self.session.query(self.Product).filter_by(product_id=product_id):
            result.append(row2dict(row))
        return result[0]

    def update(self, product_id, object):
        element = self.get(product_id)
        for key, value in object.items():
            if value != None:
                element[key] = value

        with engine.connect() as conn:
            return conn.execute(update(self.Product).where(self.Product.product_id == product_id).values(name=element["name"], price=element["price"], description=element["description"]))

class CrudInventoryProducts():
    def __init__(self):
        self.session = Session(engine)
        self.InventoryProduct = db.classes.inventory_product

    def get_all(self):
        result = []
        for row in self.session.query(self.InventoryProduct).all():
            result.append(row2dict(row))
        return result

    def get(self, inventory_id):
        result = []
        for row in self.session.query(self.InventoryProduct).filter_by(inventory_id=inventory_id):
            result.append(row2dict(row))
        return result

    def update(self, inventory_id, product_id, quantity):
        with engine.connect() as conn:
            return conn.execute(update(self.InventoryProduct).where((and_(self.InventoryProduct.inventory_id == inventory_id, self.InventoryProduct.product_id == product_id)))).values(quantity=quantity)

    def delete(self, inventory_id, product_id):
        with engine.connect() as conn:
            return conn.execute(delete(self.InventoryProduct).where((and_(self.InventoryProduct.inventory_id == inventory_id, self.InventoryProduct.product_id == product_id))))