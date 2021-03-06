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

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['newRestaurantName']
        session.commit()
        return redirect(url_for('displayRestaurants'))
    else:
        return render_template('editrestaurant.html',
        restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('displayRestaurants'))
    else:
        return render_template('deleterestaurant.html',
        restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/')
def displayMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('menuitems.html', items=items, restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('displayMenu', restaurant_id=restaurant.id))
    else:
        return render_template('deletemenuitems.html',
            item=item,
            restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_name = request.form['newMenuItemName']
        new_price = request.form['newMenuItemPrice']
        new_description = request.form['newMenuItemDescription']
        if new_name:
            item.name = new_name
        if new_price:
            item.price = new_price
        if new_description:
            item.description = new_description
        return redirect(url_for('displayMenu', restaurant_id=restaurant.id))
    else:
        return render_template('editmenuitems.html',
        restaurant=restaurant,
        item=item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=5000)
