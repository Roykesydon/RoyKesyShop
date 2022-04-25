from flask import Blueprint, Flask

from clothing.api import clothing
from user.api import user

app = Flask(__name__)


@app.route("/")
def index():
    return "HelloWorld"


app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(clothing, url_prefix="/clothing")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
