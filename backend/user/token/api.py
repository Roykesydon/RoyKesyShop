import jwt
from flask import Blueprint, request

token = Blueprint("token", __name__)


@token.route("/", methods=["POST"])
def createToken():
    return jwt.encode({"k123": "v123"}, "secret", algorithm="HS256")


@token.route("/", methods=["GET"])
def test():
    try:
        data = jwt.decode(
            request.headers["Authorization"].replace("Bearer ", ""),
            "secret",
            algorithms="HS256",
        )
    except:
        return {"success": 0, "msg": "valid error"}

    return {"success": 1, "msg": ""}
