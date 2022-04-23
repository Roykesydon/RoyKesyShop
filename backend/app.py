from flask import Blueprint, Flask

from user.api import user

app = Flask(__name__)


@app.route("/")
def index():
    return "HelloWorld"


app.register_blueprint(user, url_prefix="/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
