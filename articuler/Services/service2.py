from flask import Flask
from flask_restful import Resource, Api
import psycopg2
import pyodbc
#from DatabaseLayer.database import *


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
    def select_all_price(self):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT p1."productId", p1."productName",  p1."price" FROM "Product" p1')
            rows = cursor.fetchall()
        return rows
    def select_all_desc(self, i):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT p1."productId", p1."productName", p1."descriptionN", p1."price" FROM "Product" p1 WHERE p1."productId" =%d'%i)
            rows = cursor.fetchall()
        return rows




class Prices(Resource):
    #parser = reqparse.RequestParser()
    def get(self):
        db = SingletonDB()
        all_products = db.select_all_price()
        my_list = []
        for row in all_products:
            a = {"productId": row[0], "productName": row[1],  "price": row[2]}
            my_list.append(a)
        return my_list

class Descript(Resource):
    #parser = reqparse.RequestParser()
    def get(self, id):
        db = SingletonDB()
        all_products = db.select_all_desc(id)
        my_list = []
        for row in all_products:
            a =  {"productId": row[0], "productName": (row[1]), "descriptionN": (row[2]), "price": row[3]}
            my_list.append(a)

        return my_list[0]


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Prices, '/price-list/')
    api.add_resource(Descript, '/details/<int:id>')
    app.run(port=5002, debug=True)
