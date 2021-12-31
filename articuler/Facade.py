from flask_restful import reqparse
from BusinessLayer.ProductBuilder import Director, OwnProductBuilder, Service1ProductBuilder, Service2ProductBuilder, OwnProduct
from PersistanceLayer.SingletonDataBase import Singleton



class Facade:
    def __init__(self):
        self.director = Director()
        self.db = Singleton()
        self.parser = reqparse.RequestParser()
        self.empty_product = OwnProduct()
    def get_prod(self):
        director = Director()
        builder = OwnProductBuilder()
        self.director.builder = builder
        self.director.build_filtered_product()
        own = builder.product

        builder = Service1ProductBuilder()
        self.director.builder = builder
        self.director.build_filtered_product()
        service1 = builder.product

        builder = Service2ProductBuilder()
        self.director.builder = builder
        self.director.build_filtered_product()
        service2 = builder.product
        own.join(service1)
        own.join(service2)
        return own.products
    def insert(self):
        self.parser.add_argument("productName")
        self.parser.add_argument("descriptionN")
        self.parser.add_argument("price")

        args = self.parser.parse_args()
        self.empty_product.insert(args)
    def delete(self):
        self.parser.add_argument("productId")
        args = self.parser.parse_args()
        self.empty_product.delete(args["productId"])
    def update(self):
        self.parser.add_argument("productId")
        self.parser.add_argument("productName")
        self.parser.add_argument("descriptionN")
        self.parser.add_argument("price")

        args = self.parser.parse_args()
        self.empty_product.update(args)
