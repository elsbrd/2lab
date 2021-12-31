from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from PersistanceLayer.SingletonDataBase import Singleton
import requests
from PresentationLayer.SpecificationFilter import  MaxPrice, MinPrice, ProductName
import pyodbc

class ProductBuilder(ABC):
    @property
    @abstractmethod
    def product(self) -> None:
        pass
    @abstractmethod
    def extract_from_source(self) ->None:
        pass
    @abstractmethod
    def reformat(self) -> None:
        pass
    @abstractmethod
    def filter(self) -> None:
        pass


class Service1ProductBuilder(ProductBuilder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._product = OwnProduct()
    @property
    def product(self) -> OwnProduct:
        product = self._product
        self.reset()
        return product
    def extract_from_source(self) ->None:
        self._product.set(requests.get('http://127.0.0.1:5001/search/').json())
    def reformat(self) -> None:
        pass
    def filter(self) -> None:
        self._product.filter()
class Service2ProductBuilder(ProductBuilder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._product = OwnProduct()
    @property
    def product(self) -> OwnProduct:
        product = self._product
        self.reset()
        return product
    def extract_from_source(self) ->None:
        self._product.set(requests.get('http://127.0.0.1:5002/price-list/').json())
    def reformat(self) -> None:
        full_products = []
        for row in self._product.products:
            full_products.append(requests.get('http://127.0.0.1:5002/details/'+str(row["productId"])).json())
        self._product.set(full_products)
    def filter(self) -> None:
        self._product.filter()

class OwnProductBuilder(ProductBuilder):
    def __init__(self) -> None:
        self.reset()
        self.db = Singleton()
    def reset(self) -> None:
        self._product = OwnProduct()
    @property
    def product(self) -> OwnProduct:
        product = self._product
        self.reset()
        return product
    def extract_from_source(self) ->None:
        self._product.set(self._product.select_all_prod())
    def reformat(self) -> None:
        my_list = []
        for row in self.product.products:
            a = {"productId": row[0], "productName": (row[1]), "descriptionN": (row[2]), "price": row[3]}
            my_list.append(a)
        self._product.set(my_list)
    def filter(self) -> None:
        self._product.filter()
class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> builder:
        return self._builder

    @builder.setter
    def builder(self, builder: builder) -> None:
        self._builder = builder

    def build_all_product(self) -> None:
        self.builder.extract_from_source()
        self.builder.reformat()
    def build_filtered_product(self) -> None:
        self.builder.extract_from_source()
        self.builder.reformat()
        self.builder.filter()
class OwnProduct():
    def __init__(self):
        self.products = []
        self.conn = Singleton().conn
    def add(self, product: dict[str, Any]):
        self.products.append(product)
    def join(self, another_product):
        self.products += another_product.products
    def drop(self, id):
        del self.products[id]
    def set(self, products):
        self.products = products
    def select_all_prod(self):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT p1."productId", p1."productName",p1."descriptionN",  p1."price" FROM "Product" p1')
            rows = cursor.fetchall()
        return rows
    def insert(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO [Product] ([productName], [descriptionN], [price]) VALUES('%s','%s','%s')'''%(str(args["productName"]), str(args["descriptionN"]), str(args["price"])))
        self.conn.commit()
    def delete(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM "Product" WHERE "productId"='+str(id))
        self.conn.commit()

    def update(self, args):
        query_str = 'UPDATE "Product" SET '
        for key, value in args.items():
            if key != 'productId' and value !=None:
                query_str += '"' + key + '"=' + "'" + str(value) + "',"
        query_str = query_str[0:-1]
        query_str += ' WHERE "productId"=' + str(args["productId"])
        with self.conn.cursor() as cursor:
            cursor.execute(query_str)
        self.conn.commit()

    def filter(self):
        product_filter = MaxPrice() & MinPrice() & ProductName()
        products = []
        for i in self.products:
            if product_filter.is_satisfied_by(i):
                products.append(i)
        self.products = products
