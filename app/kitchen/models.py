from app.db import db, BaseModelMixin

# orders


class StatusOrder(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    orders = db.relationship('Order', backref='StatusOrder', lazy=True)


class Order(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())
    status_order_id = db.Column(db.Integer, db.ForeignKey(
        'status_order.id'), nullable=False)
    client_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    order_menu = db.relationship('OrderMenu', back_populates="order")

    def __repr__(self):
        return f'<Order {self.id}>'

    def __str__(self):
        return f'<Order {self.id}>'


class OrderMenu(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

    order = db.relationship('Order', back_populates="order_menu")
    menu = db.relationship('Menu', back_populates="order_menu")
    # order_menu_extras = db.relationship('OrderMenuExtras', back_populates="order_menu")

    orders_extras = db.relationship(
        'OrderMenuExtras', backref='Orders', lazy=True)

    def __repr__(self):
        return f'<OrderMenu {self.id}>'

    def __str__(self):
        return f'<OrderMenu {self.id}'

# menu


class Menu(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=True)

    # order_menu = db.relationship('OrderMenu', backref="Menu", lazy=True)
    order_menu = db.relationship('OrderMenu', back_populates="menu")

# extras


class ExtrasCategory(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    extras = db.relationship('Extras', backref='ExtrasCategory', lazy=True)


class Extras(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    price = db.Column(db.Float, nullable=False)
    extras_category_id = db.Column(db.Integer, db.ForeignKey(
        'extras_category.id'), nullable=False)

    orders_extras = db.relationship(
        'OrderMenuExtras', backref='Extras', lazy=True)

# orders extras


class OrderMenuExtras(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    order_menu_id = db.Column(db.Integer, db.ForeignKey(
        'order_menu.id'), nullable=True)
    extra_id = db.Column(db.Integer, db.ForeignKey(
        'extras.id'), nullable=False)

    # # populates
    # order_menu = db.relationship('OrderMenu', back_populates="order_menu_extras")