import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Restaurant, MenuItem

Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

"""
items = session.query(MenuItem).all()
for item in items:
    print item.name
"""

print "veggie burgers in the db:"
burgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for burger in burgers:
    print burger.id
    print burger.price
    print burger.restaurant.name
    print "\n"


print "urban burger:"
urbanBurger = session.query(MenuItem).filter_by(id = 8).one()
print urbanBurger.price
print urbanBurger.restaurant.name
print "\n"

urbanBurger.price = '$2.99'
session.add(urbanBurger)
session.commit()

print "urban burger price changed!:"
urbanBurger = session.query(MenuItem).filter_by(id = 8).one()
print urbanBurger.price
print urbanBurger.restaurant.name
print "\n"

for burger in burgers:
    if burger.price != '$2.99':
        burger.price = '$2.99'
        session.add(burger)
        session.commit()

print "Now everyone changed their price too:"
burgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for burger in burgers:
    print burger.id
    print burger.price
    print burger.restaurant.name
    print "\n"

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream')
if (len(spinach.all()) > 0):
    spinach = spinach.one()
    print spinach.name
    print "at"
    print spinach.restaurant.name
    session.delete(spinach)
    session.commit()
    spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream')
    print "Spinach ice cream occurs %(num)02d times now" % {num:
            len(spinach.all())}
