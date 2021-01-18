import uuid
import datetime
import requests
from common.database import Database
import models.alerts.constants as AlertConstants
from models.items.item import Item
import os

class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.active = active
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        
        if self.item.price < self.price_limit:
            print("Price limit reached for {}. Sending email to {}".format(self.item.name, self.user_email))
            self.send()
        else:
            print("Price limit NOT reached for {}".format(self.item.name))

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})

    def send(self):

        #URL = os.environ.get('URL')
        #API_KEY = os.environ.get('API_KEY')
        print(AlertConstants.API_KEY)
        print(AlertConstants.URL)

        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={"from": "Mailgun Sandbox <postmaster@sandbox2eefabb923604faea7686b1eac2f5b5e.mailgun.org>",
                  "to": self.user_email,
                 "subject": "Price limit reached for {}".format(self.item.name),
                 "text": "We've found a deal! ({}).".format(self.item.url)})


    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit},
                                                       "active": True
                                                       })]

