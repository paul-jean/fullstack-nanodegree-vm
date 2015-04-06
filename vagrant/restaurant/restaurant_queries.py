import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import insert
from sqlalchemy import create_engine, distinct
from database_setup import Restaurant, MenuItem

Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def get_restaurants():
    name_id = [(r.id, r.name) for r in \
            session.query(Restaurant).\
            order_by(Restaurant.name).\
            distinct(Restaurant.name).\
            group_by(Restaurant.name).all()]
    return name_id

def add_restaurant(restaurant_name):
    new_restaurant = Restaurant(name = restaurant_name)
    session.add(new_restaurant)
    session.commit()

def restaurant_exists(restaurant_name):
    found = session.query(Restaurant).filter_by(name = restaurant_name).all()
    return len(found) >= 1

def test():
    rs = get_restaurants()
    for r in rs:
        print r
