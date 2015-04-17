from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem

# init Flask
app = Flask(__name__)

# init SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/')
def menuItems(restaurant_id):
    rest = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest.id).all()
    return render_template("menu.html", restaurant=rest, items=items)

@app.route("/restaurant/<int:rest_id>/new/")
def newMenuItem(rest_id):
    return "new menu item"

@app.route("/restaurant/<int:rest_id>/<int:menu_id>/edit/")
def editMenuItem(rest_id, menu_id):
    return "edit menu item"

@app.route("/restaurant/<int:rest_id>/<int:menu_id>/delete/")
def deleteMenuItem(rest_id, menu_id):
    return "delete menu item"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
