#import psycopg2
import pyodbc
#from DatabaseLayer.database import *

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=LAPTOP-KML4VGQE\ELSBRD;'
                                   'Database=furnitureShop;'
                                   'Trusted_Connection=yes;')