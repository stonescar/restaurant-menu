from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import (Flask, render_template, request,
                   redirect, url_for, jsonify, flash)
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash('New restaurant (%s) created' % restaurant.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant.id))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('%s edited' % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('%s deleted' % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    appetizers = session.query(MenuItem).filter_by(
        restaurant=restaurant, course='Appetizer')
    entrees = session.query(MenuItem).filter_by(
        restaurant=restaurant, course='Entree')
    desserts = session.query(MenuItem).filter_by(
        restaurant=restaurant, course='Dessert')
    beverages = session.query(MenuItem).filter_by(
        restaurant=restaurant, course='Beverage')
    items = [appetizers, entrees, desserts, beverages]
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        course = request.form['course']
        description = request.form['description']
        item = MenuItem(name=name,
                        price=price,
                        course=course,
                        description=description,
                        restaurant=restaurant)
        session.add(item)
        session.commit()
        flash('New menu item (%s) created' % name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.course = request.form['course']
        item.description = request.form['description']
        session.add(item)
        session.commit()
        flash('%s edited' % item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('%s deleted' % item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=item)


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
