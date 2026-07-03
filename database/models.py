# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    items_id = db.Column(db.ForeignKey('menu_item.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    items = db.relationship('MenuItem', primaryjoin='Cart.items_id == MenuItem.id', backref='carts')
    users = db.relationship('User', primaryjoin='Cart.users_id == User.id', backref='carts')



class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img_filename = db.Column(db.String(225), nullable=False, server_default=db.FetchedValue())



class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    id = db.Column(db.Integer, primary_key=True)
    resturant_id = db.Column(db.ForeignKey('resturant_owner.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(225), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.ForeignKey('images.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    image = db.relationship('Image', primaryjoin='MenuItem.image_id == Image.id', backref='menu_items')
    resturant = db.relationship('ResturantOwner', primaryjoin='MenuItem.resturant_id == ResturantOwner.id', backref='menu_items')



class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    resturant_id = db.Column(db.ForeignKey('resturant_owner.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    total_amount = db.Column(db.Numeric(10, 0), nullable=False)
    status = db.Column(db.Enum('pending', 'preparing', 'order-complete'), nullable=False)
    delivery_address = db.Column(db.String(225), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    client = db.relationship('User', primaryjoin='Order.client_id == User.id', backref='orders')
    resturant = db.relationship('ResturantOwner', primaryjoin='Order.resturant_id == ResturantOwner.id', backref='orders')



class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    menu_item_id = db.Column(db.ForeignKey('menu_item.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 0), nullable=False)

    menu_item = db.relationship('MenuItem', primaryjoin='OrderItem.menu_item_id == MenuItem.id', backref='order_items')
    order = db.relationship('Order', primaryjoin='OrderItem.order_id == Order.id', backref='order_items')



class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey('order.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    amount = db.Column(db.Numeric(10, 0), nullable=False)
    payment_method = db.Column(db.Enum('e-sewa', 'online-banking', 'ime/khalti pay'), nullable=False)
    payment_info = db.Column(db.String(225), nullable=False)
    status = db.Column(db.Enum('pending', 'cleared', 'error'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    order = db.relationship('Order', primaryjoin='Payment.order_id == Order.id', backref='payments')



class ResturantOwner(db.Model):
    __tablename__ = 'resturant_owner'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    pass_hass = db.Column(db.String(225), nullable=False)
    address = db.Column(db.String(225), nullable=False)
    is_active = db.Column(db.Integer)
    email = db.Column(db.String(225), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    role = db.Column(db.Enum('user', 'resturant', 'admin'), nullable=False)



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    pass_hass = db.Column(db.String(225), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(225), nullable=False)
    role = db.Column(db.Enum('user'), nullable=False)
