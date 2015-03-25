import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Restaurant

Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()
cheesepizze = MenuItem(
	name = "Cheese Pizza", 
	description = "Made with all natural ingredients", 
	course = "Entree", 
	price = "$8.99", 
	restaurant = myFirstRestaurant)
session.commit()
session.query(MenuItem).all()

