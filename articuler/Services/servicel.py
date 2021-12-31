from flask import Flask
from flask_restful import Resource, Api
import psycopg2
#from DatabaseLayer.database import *
from PresentationLayer.SpecificationFilter import MaxPrice, MinPrice, ProductName
import PresentationLayer.SpecificationFilter
import pyodbc

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class SingletonDB(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=LAPTOP-KML4VGQE\ELSBRD;'
                                   'Database=furnitureShop;'
                                   'Trusted_Connection=yes;')
    def select_all_prod(self):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT p1."productId", p1."productName",p1."descriptionN",  p1."price" FROM "product" p1')
            rows = cursor.fetchall()
        return rows




class Products(Resource):
    #parser = reqparse.RequestParser()
    def get(self):
        db = SingletonDB()
        all_products = db.select_all_prod()
        my_list = []
        for row in all_products:
            a = {"productId": row[0], "productName": (row[1]), "descriptionN": (row[2]), "price": row[3]}
            my_list.append(a)
        all_products.clear()

        product_filter = MaxPrice() & MinPrice() & ProductName()
        products = []
        for i in my_list:

            if product_filter.is_satisfied_by(i):
                products.append(i)
        return products

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Products, '/search/')
    app.run(port=5001, debug=True)