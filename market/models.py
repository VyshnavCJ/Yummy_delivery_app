from market import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    real_name = db.StringField(required=True)
    email_address = db.StringField(required=True, unique=True)
    phone_num = db.IntField(required=True, unique=True)
    role = db.IntField(required=True)
    address = db.StringField(required=True)
    password_hash = db.StringField(required=True, max_length=60)


class Item(db.Document):
    meta = {'abstract': True}
    name = db.StringField(max_length=30, required=True)
    price = db.IntField(required=True)
    quantity = db.IntField(required=True)

    def __repr__(self):
        return f'Item {self.name}'

    def can_purchase(self, given_quantity):
        return self.quantity >= given_quantity

    def quantity_decrease(self, given_quantity):
        self.quantity -= given_quantity


class Customer(Item):
    status = db.IntField(default=-1, required=True)
    owner = db.StringField(required=True)
    hotel_user = db.StringField(required=True)

    def user_buy(self, user):
        self.owner = user.username

    def accepted(self):
        self.status = 0

    def received(self):
        self.status = 1


class Hotel(Item):
    owner = db.StringField(required=True)

    def add(self, user):
        self.owner = user.username

    def update(self, price, quantity):
        self.price = price
        self.quantity = quantity
