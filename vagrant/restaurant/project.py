from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/restaurants/<int:rest_id>/')
def menuItems(rest_id):
    rest = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest.id).all()
    return render_template('menu.html', restaurant=rest, items=items)

@app.route('/restaurant/<int:rest_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(rest_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = rest_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('menuItems', rest_id = rest_id))
    else:
        return render_template('new-menu-item.html', restaurant_id = rest_id)

@app.route('/restaurant/<int:rest_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(rest_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('menuItems', rest_id = rest_id))
    else:
        return render_template('edit-menu-item.html', restaurant_id = rest_id, menu_id = menu_id, item = editedItem)

@app.route('/restaurant/<int:rest_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(rest_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('menuItems', rest_id = rest_id))
    else:
        return render_template('delete-menu-item.html', restaurant_id = rest_id, menu_id = menu_id, item = deletedItem)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
