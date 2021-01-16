from flask import Flask, render_template
from common.database import Database
from models.users.views import user_blueprint

from models.stores.views import store_blueprint
from models.alerts.views import alert_blueprint

import os


app = Flask(__name__)
app.config.from_object('src.config')
#Below works if we have a '.env' in the root project folder
#app.config.update(
#    ADMIN=os.environ.get('ADMIN')
#)

print(app.config['ADMIN'])

app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')
    #return "<h1>Hello</H1>"


app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")

#if __name__ == '__main__':
#   print("Run!")
#   app.run(port=4995, debug=True)
