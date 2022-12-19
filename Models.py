from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]

    def to_json(self):
        result = {
            "id": self.id,
            "name": self.name,
        }
        return result


class Vendors(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.name = data["name"]

    def to_json(self):
        result = {
            "id": self.id,
            "name": self.name,
        }
        return result


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    model = Column(String)
    specs = Column(String)
    price = Column(Integer)
    warranty_period = Column(Integer)
    image = Column(String)

    category = relationship("Categories")
    vendor = relationship("Vendors")
    shopping_cart = relationship("ShoppingCart", backref="orders_cart")

    def __init__(self, data, session):
        self.id = data["id"]
        self.category = session.query(Categories).get(data["category"]["id"])
        self.vendor = session.query(Vendors).get(data["vendor"]["id"])
        self.category_id = data["category"]["id"]
        self.vendor_id = data["vendor"]["id"]
        self.model = data["model"]
        self.specs = data["specs"]
        self.price = data["price"]
        self.warranty_period = data["warranty_period"]
        self.image = data["image"]

    def to_json(self):
        result = {
            "id": self.id,
            "category": self.category.to_json(),
            "vendor": self.vendor.to_json(),
            "model": self.model,
            "specs": self.specs,
            "price": self.price,
            "warranty_period": self.warranty_period,
            "image": self.image,
        }
        return result


class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    contact_number = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.contact_number = data["contact_number"]

    def to_json(self):
        result = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "contact_number": self.contact_number

        }
        return result


class Stores(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    paid_delivery = Column(Boolean)

    def __init__(self, data, session):
        self.id = data["id"]
        self.email = data["email"]
        self.paid_delivery = data["paid_delivery"]

    def to_json(self):
        result = {
            "id": self.id,
            "email": self.email,
            "paid_delivery": self.paid_delivery,

        }
        return result


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))
    order_date = Column(Date)
    order_time = Column(Time)
    confirmation = Column(Boolean)

    client = relationship("Clients")
    store = relationship("Stores")
    shopping_cart = relationship("ShoppingCart", backref="products_cart")

    def __init__(self, data, session):
        self.id = data["id"]
        self.client = session.query(Clients).get(data["client"]["id"])
        self.store = session.query(Stores).get(data["store"]["id"])
        self.client_id = data["client"]["id"]
        self.store_id = data["store"]["id"]
        self.order_date = data["order_date"]
        self.order_time = data["order_time"]
        self.confirmation = data["confirmation"]

    def to_json(self):
        result = {
            "id": self.id,
            "client": self.client.to_json(),
            "store": self.store.to_json(),
            "order_date": str(self.order_date),
            "order_time": str(self.order_time),
            "confirmation": self.confirmation,
        }
        return result


class Couriers(Base):
    __tablename__ = "couriers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    contact_number = Column(String)

    def __init__(self, data, session):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.contact_number = data["contact_number"]

    def to_json(self):
        result = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "contact_number": self.contact_number

        }
        return result


class Delivery(Base):
    __tablename__ = "delivery"
    id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey("couriers.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    delivery_date = Column(Date)
    delivery_time = Column(Time)
    delivery_address = Column(String)

    courier = relationship("Couriers")
    order = relationship("Orders")

    def __init__(self, data, session):
        self.id = data["id"]
        self.courier = session.query(Couriers).get(data["courier"]["id"])
        self.order = session.query(Orders).get(data["order"]["id"])
        self.courier_id = data["courier"]["id"]
        self.order_id = data["order"]["id"]
        self.delivery_date = data["delivery_date"]
        self.delivery_time = data["delivery_time"]
        self.delivery_address = data["delivery_address"]

    def to_json(self):
        result = {
            "id": self.id,
            "courier": self.courier.to_json(),
            "order": self.order.to_json(),
            "delivery_date": str(self.delivery_date),
            "delivery_time": str(self.delivery_time),
            "delivery_address": self.delivery_address

        }
        return result


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    amount = Column(Integer)

    order = relationship("Orders")
    product = relationship("Products")

    def __init__(self, data, session):
        self.id = data["id"]
        self.order = session.query(Orders).get(data["order"]["id"])
        self.product = session.query(Products).get(data["product"]["id"])
        self.order_id = data["order"]["id"]
        self.product_id = data["product"]["id"]
        self.amount = data["amount"]

    def to_json(self):
        result = {
            "id": self.id,
            "order": self.order.to_json(),
            "product": self.product.to_json(),
            "amount": self.amount

        }
        return result
