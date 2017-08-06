from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import distinct

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# Main Page
@app.route('/')
@app.route('/restaurants/')
def displayRestaurants():
    items = session.query(Restaurant).all()
    return render_template('restaurants.html', items=items)

# Add New Restaurant
@app.route('/restaurants/new/', methods=['GET', 'POST'])
def addNewRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['newRestaurantName'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('displayRestaurants'))
    else:
        return render_template('addrestaurant.html')



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=5000)
