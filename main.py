import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SECRET_KEY'] = 'blahblah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")

    

## HTTP GET - Read Record
@app.route('/random', methods=['GET'])
def read_random():
    coffee_shops = Cafe.query.all()
    i = random.choice(coffee_shops)
    coffee_shop_data = {
            'name': i.name,
            'map_url': i.map_url,
            'img_url': i.img_url,
            'location': i.location,
            'has_sockets': i.has_sockets,
            'has_toilet': i.has_toilet,
            'has_wifi': i.has_wifi,
            'can_take_calls': i.can_take_calls,
            'seats': i.seats,
            'coffee_price': i.coffee_price
    }
    return jsonify(cafes=coffee_shop_data)

@app.route('/all')
def read_all():
    coffee_shops = Cafe.query.all()
    all_shops = []
    for i in coffee_shops:
        coffee_shop_data = {
            'name': i.name,
            'map_url': i.map_url,
            'img_url': i.img_url,
            'location': i.location,
            'has_sockets': i.has_sockets,
            'has_toilet': i.has_toilet,
            'has_wifi': i.has_wifi,
            'can_take_calls': i.can_take_calls,
            'seats': i.seats,
            'coffee_price': i.coffee_price
        }
        all_shops.append(coffee_shop_data)
    return jsonify(cafes=all_shops)

@app.route('/search', methods=['GET'])
def cafe_search_by_location():
    location_bad = request.query_string.decode().split('=')
    location = location_bad[1]
    all_cafes = []
    cafes_of_that_location = Cafe.query.filter_by(location=location).all()
    if len(cafes_of_that_location) > 0:
        for i in cafes_of_that_location:
            coffee_shop_data = {
                'name': i.name,
                'map_url': i.map_url,
                'img_url': i.img_url,
                'location': i.location,
                'has_sockets': i.has_sockets,
                'has_toilet': i.has_toilet,
                'has_wifi': i.has_wifi,
                'can_take_calls': i.can_take_calls,
                'seats': i.seats,
                'coffee_price': i.coffee_price
            }
            all_cafes.append(coffee_shop_data)
        return jsonify(cafes=all_cafes)
    else:
        error = {
            'Not Found': 'Sorry, We don\'t have Cafe at that Location'
        }
        return jsonify(error=error)

## HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add():
    no_of_shops_then = len(Cafe.query.all())
    if request.method == 'POST':
        new_cafe = Cafe(id=no_of_shops_then+1, name=request.form['name'], map_url=request.form['map_url'],img_url=request.form['img_url'],location=request.form['location'],has_sockets=bool(request.form['has_sockets']),has_toilet=bool(request.form['has_toilet']),has_wifi=bool(request.form['has_wifi']),can_take_calls=bool(request.form['can_take_calls']),seats=request.form['seats'],coffee_price=request.form['coffee_price'])
        db.session.add(new_cafe)
        db.session.commit()
        no_of_shops_now = len(Cafe.query.all())
        if no_of_shops_now - no_of_shops_then:
            success = {
                'success': 'Successfully added the Cafe Details'
            }
        else:
            success = {
                'failure': 'Failed to add the Cafe Details'
            }
        return jsonify(response=success)


## HTTP PUT/PATCH - Update Record

@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_the_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    price_bad = request.query_string.decode().split('=')
    price = price_bad[1]
    if cafe is None:
        err = {
            'Not Found': 'Cafe Shop of that ID doesn\'t exist'
        }
        return jsonify(error=err),404
    else:
        cafe.coffee_price = price
        db.session.commit()
        return jsonify(response={'success':"Price successfully changed"}),200

## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    key = request.args.get('api-key')
    if key == "TopSecretAPIKey" and cafe is not None:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={'success': f'Cafe with the ID of {cafe_id} has been deleted successfully'})
    elif key != 'TopSecretAPIKey':
        return jsonify(response={'Key Error': 'The Key which you\'ve entered is Wrong. Please try again'})
    else:
        return jsonify(response={'Not Found': 'Cafe with that ID doesn\'t exist'})

if __name__ == '__main__':
    app.run(debug=True)
