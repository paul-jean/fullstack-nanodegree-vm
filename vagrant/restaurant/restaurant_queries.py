import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, distinct
from database_setup import Restaurant, MenuItem

Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def get_restaurants():
    names = session.query(Restaurant.name).\
            order_by(Restaurant.name).\
            distinct(Restaurant.name).all()
    for i in range(len(names)):
        names[i] = names[i][0]
    return names

def test():
    rs = get_restaurants()
    for r in rs:
        print r
