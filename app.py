from datetime import datetime
import sqlalchemy as db
from flask import Flask, request, make_response, jsonify, abort
import json
from sqlalchemy.orm import sessionmaker
from Models import *
from flask_swagger_ui import get_swaggerui_blueprint

engine = db.create_engine('postgresql+psycopg2://postgres:19092001@localhost/PGDB')

conn = engine.connect()

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

Session = sessionmaker(bind=engine)
session = Session()

models = {
    "categories": Categories,
    "vendors": Vendors,
    "products": Products,
    "clients": Clients,
    "stores": Stores,
    "orders": Orders,
    "couriers": Couriers,
    "delivery": Delivery,
    "shopping_cart": ShoppingCart
}


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/rest/list', methods=['POST'])
def get_list():
    if not request.json or not 'table_name' in request.json:
        abort(400)
    data = request.json
    query = session.query(models[data['table_name']])
    try:
        offset_value = int(data["offset_value"])
        if offset_value > 0:
            query = query.offset(offset_value)
    except:
        print("An exception occurred")
    try:
        limit_value = int(data["limit_value"])
        if limit_value > 0:
            query = query.limit(limit_value)
    except:
        print("An exception occurred")
    result = []
    for entity in query:
        result.append(entity.to_json())
    return json.dumps(result)


def get_by_id(class_, id_):
    obj = session.query(class_).get(id_)
    return json.dumps(obj.to_json())


@app.route("/rest/get", methods=['POST'])
def get_entity():
    if not request.json or not 'table_name' in request.json:
        abort(400)
    data = request.json
    entity_id = int(data["id"])
    if data["table_name"] in models:
        return get_by_id(models[request.json["table_name"]], entity_id)
    return json.dumps(entity_id)


def update_entity(class_, data):
    obj = class_(data, session)
    if obj.id == -1:
        obj.id = None
    if obj.id is None:
        session.add(obj)
    else:
        session.merge(obj)
    session.commit()
    return str(obj.id)


@app.route("/rest/update", methods=["POST"])
def upsert():
    data = request.json
    if data["table_name"] in models:
        try:
            return update_entity(models[data["table_name"]], data["obj"])
        except:
            session.rollback()
    return json.dumps("False")


def delete_entity(class_, id_):
    session.query(class_).filter(class_.id == id_).delete()
    session.commit()


@app.route("/rest/delete", methods=["POST"])
def delete():
    data = request.json
    if data["table_name"] in models:
        try:
            delete_entity(models[data["table_name"]], int(data["obj"]["id"]))
            return json.dumps("Success!")
        except:
            session.rollback()
    return json.dumps("Fail!")


@app.route("/rest/get_size/<string:table_name>", methods=["GET"])
def get_rows(table_name):
    try:
        rows = session.query(models[table_name]).count()
        return json.dumps(rows)
    except:
        return json.dumps("Error!")


"""
Search
Categories
"""


@app.route("/rest/categories/get_by_name/<string:input_name>", methods=["GET"])
def category_get_by_name(input_name):
    result = session.query(Categories).filter(Categories.name == input_name)
    out = []
    for entity in result:
        out.append(entity.to_json())
        return json.dumps(out)
    return json.dumps({})


@app.route("/rest/categories/search_by_name/<string:input_name>", methods=["GET"])
def category_search_by_name(input_name):
    query = session.query(models["categories"])
    query = query.all()
    result = []
    for entity in query:
        if input_name.lower() in entity.name.lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Vendors
"""


@app.route("/rest/vendors/get_by_name/<string:input_name>", methods=["GET"])
def vendor_get_by_name(input_name):
    result = session.query(Vendors).filter(Vendors.name == input_name)
    out = []
    for entity in result:
        out.append(entity.to_json())
        return json.dumps(out)
    return json.dumps({})


@app.route("/rest/vendors/search_by_name/<string:input_name>", methods=["GET"])
def vendor_search_by_name(input_name):
    query = session.query(models["vendors"])
    query = query.all()
    result = []
    for entity in query:
        if input_name.lower() in entity.name.lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Products
"""


@app.route("/rest/products/search_by_category_id/<int:input>", methods=["GET"])
def product_search_by_category_id(input):
    query = session.query(models["products"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.category_id:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/products/search_by_vendor_id/<int:input>", methods=["GET"])
def product_search_by_vendor_id(input):
    query = session.query(models["products"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.vendor_id:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/products/search_by_model/<string:input>", methods=["GET"])
def product_search_by_model(input):
    query = session.query(models["products"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.model.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/products/search_by_specs/<string:input>", methods=["GET"])
def product_search_by_specs(input):
    query = session.query(models["products"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.specs.lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Stores
"""


@app.route("/rest/stores/get_by_email/<string:input_email>", methods=["GET"])
def store_get_by_email(input_email):
    result = session.query(Stores).filter(Stores.email == input_email)
    out = []
    for entity in result:
        out.append(entity.to_json())
        return json.dumps(out)
    return json.dumps({})


@app.route("/rest/stores/search_by_email/<string:input_email>", methods=["GET"])
def stores_search_by_email(input_email):
    query = session.query(models["stores"])
    query = query.all()
    result = []
    for entity in query:
        if input_email.lower() in entity.email.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/stores/search_by_paid_delivery/<string:input_paid_delivery>", methods=["GET"])
def stores_search_by_paid_delivery(input_paid_delivery):
    query = session.query(models["stores"])
    query = query.all()
    result = []
    for entity in query:
        if input_paid_delivery.lower() in str(entity.paid_delivery).lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Clients
"""


@app.route("/rest/clients/search_by_firstname/<string:input>", methods=["GET"])
def client_search_by_firstname(input):
    query = session.query(models["clients"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.first_name.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/clients/search_by_lastname/<string:input>", methods=["GET"])
def client_search_by_lastname(input):
    query = session.query(models["clients"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.last_name.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/clients/search_by_email/<string:input>", methods=["GET"])
def client_search_by_email(input):
    query = session.query(models["clients"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.email.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/clients/search_by_contact_number/<string:input>", methods=["GET"])
def client_search_by_phone(input):
    query = session.query(models["couriers"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.contact_number.lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Orders
"""


@app.route("/rest/orders/search_by_client_id/<int:input>", methods=["GET"])
def order_search_by_client_id(input):
    query = session.query(models["orders"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.client_id:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/orders/search_by_order_id/<int:input>", methods=["GET"])
def order_search_by_store_id(input):
    query = session.query(models["orders"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.store_id:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/orders/search_by_date/<string:date>", methods=["GET"])
def order_search_by_date(date):
    query = session.query(models["orders"])
    query = query.all()

    date_ = datetime.strptime(date, '%Y-%m-%d').date()

    result = []
    for entity in query:
        target = datetime.strptime(str(entity.order_date), '%Y-%m-%d').date()
        if date_ == target:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/orders/search_by_time/<string:left>/<string:right>", methods=["GET"])
def order_search_by_time(left, right):
    query = session.query(models["orders"])
    query = query.all()

    date_left = datetime.strptime(left, '%H:%M:%S').time()
    date_right = datetime.strptime(right, '%H:%M:%S').time()

    result = []
    for entity in query:
        target = datetime.strptime(str(entity.order_time), '%H:%M:%S').time()
        if date_left < target < date_right:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/orders/search_by_confirmation/<string:input_confirmation>", methods=["GET"])
def order_search_by_confirmation(input_confirmation):
    query = session.query(models["orders"])
    query = query.all()
    result = []
    for entity in query:
        if input_confirmation.lower() in str(entity.confirmation).lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Couriers
"""


@app.route("/rest/couriers/search_by_firstname/<string:input>", methods=["GET"])
def courier_search_by_firstname(input):
    query = session.query(models["couriers"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.first_name.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/couriers/search_by_lastname/<string:input>", methods=["GET"])
def courier_search_by_lastname(input):
    query = session.query(models["couriers"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.last_name.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/couriers/search_by_email/<string:input>", methods=["GET"])
def courier_search_by_email(input):
    query = session.query(models["couriers"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.email.lower():
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/couriers/search_by_contact_number/<string:input>", methods=["GET"])
def courier_search_by_phone(input):
    query = session.query(models["couriers"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.contact_number.lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Delivery
"""


@app.route("/rest/delivery/search_by_courier_id/<int:input>", methods=["GET"])
def delivery_search_by_courier_id(input):
    query = session.query(models["delivery"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.courier_id:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/delivery/search_by_order_id/<int:input>", methods=["GET"])
def delivery_search_by_order_id(input):
    query = session.query(models["delivery"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.order_id:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/delivery/search_by_date/<string:date>", methods=["GET"])
def delivery_search_by_date(date):
    query = session.query(models["delivery"])
    query = query.all()

    date_ = datetime.strptime(date, '%Y-%m-%d').date()

    result = []
    for entity in query:
        target = datetime.strptime(str(entity.delivery_date), '%Y-%m-%d').date()
        if date_ == target:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/delivery/search_by_time/<string:left>/<string:right>", methods=["GET"])
def delivery_search_by_time(left, right):
    query = session.query(models["delivery"])
    query = query.all()

    date_left = datetime.strptime(left, '%H:%M:%S').time()
    date_right = datetime.strptime(right, '%H:%M:%S').time()

    result = []
    for entity in query:
        target = datetime.strptime(str(entity.delivery_time), '%H:%M:%S').time()
        if date_left < target < date_right:
            result.append(entity.to_json())
    return json.dumps(result)


@app.route("/rest/delivery/search_by_delivery_address/<string:input>", methods=["GET"])
def delivery_search_by_address(input):
    query = session.query(models["delivery"])
    query = query.all()
    result = []
    for entity in query:
        if input.lower() in entity.delivery_address.lower():
            result.append(entity.to_json())
    return json.dumps(result)


"""
Shopping cart
"""


@app.route("/rest/shopping_cart/search_by_order_id/<int:input>", methods=["GET"])
def shopping_cart_search_by_order_id(input):
    query = session.query(models["shopping_cart"])
    query = query.all()
    result = []
    for entity in query:
        if input == entity.order_id:
            result.append(entity.to_json())
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True)
