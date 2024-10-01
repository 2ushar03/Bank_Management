from flask_mongoengine import MongoEngine
import datetime

db = MongoEngine()

class Customer_Account(db.Document):
    ssn_id = db.StringField(unique=True)
    customer_name = db.StringField(max_length=50)
    age = db.IntField()
    address = db.StringField(max_length=100)
    state = db.StringField()
    city = db.StringField()
    message = db.StringField()
    datetime = db.StringField()
    account_type = db.StringField(max_length=30, default='savings')
    s_m = db.IntField(default=0)
    email = db.StringField(max_length=100, unique=True)  # New field for email
    phone = db.StringField(max_length=15, unique=True)  # New field for phone number

class Transactions(db.Document):
    id_no = db.IntField(default=0)
    name = db.StringField(default='0')
    description = db.StringField(default='0')
    datetime = db.StringField(default='0')
    amount = db.IntField(default=0)