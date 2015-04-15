from flask import Flask
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

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def menuItems(restaurant_id):
    rest = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = rest.id).all()
    output = '<html><body>'
    output += '<h1>%s</h1>' % rest.name
    output += '... has %s items:' % len(items)
    output += '<br><br>'
    for i in items:
        output += i.name
        output += '<br>'
        output += i.price
        output += '<br>'
        output += i.description
        output += '<br>'
        output += '<br>'
    output += '<br>'
    output += '</body></html>'
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
