from flask import Blueprint, Flask

import utils.connection_pool as connection_pool
from clothing.api import clothing
from clothing_class.api import clothing_class
from order.api import order
from user.api import user

app = Flask(__name__)
connection_pool.init()


@app.route("/")
def index():
    return "HelloWorld"


app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(clothing, url_prefix="/clothing")
app.register_blueprint(clothing_class, url_prefix="/clothing_class")
app.register_blueprint(order, url_prefix="/order")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
