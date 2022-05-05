import base64
import hashlib
import os

from flask import Blueprint, request

from utils.config import get_config
from utils.jwt_handle import make_jwt_token
from utils.transaction_executor import TransactionExecutor
from utils.validator import Validator

user = Blueprint("user", __name__)


@user.route("/")
def index():
    return "Hello user"


@user.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    return_json = {"success": 0, "msg": "", "token": ""}

    validator = Validator()
    validator.required([email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    with TransactionExecutor() as transaction_executor:
        """
        Check whether email already been used or not
        """
        success_flag, result = transaction_executor.query_sql(
            "SELECT * from Users WHERE email = %(email)s",
            {"email": email},
            fetch_one=True,
        )

        if success_flag:
            if result != None:
                return_json["msg"] = "Email already been used"
                return return_json
        else:
            return_json["msg"] = "server error"
            return return_json

        """
        Insert user information into database
        """
        salt = os.urandom(16)
        salt = base64.b64encode(salt)

        hash_password = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 100000
        ).hex()

        insert_string = "INSERT INTO Users(name, email, salt, password) values (%(name)s, %(email)s, %(salt)s, %(password)s)"
        success_flag = transaction_executor.execute_sql(
            insert_string,
            {
                "name": None,
                "email": email,
                "salt": salt,
                "password": hash_password,
            },
        )
        if not success_flag:
            return_json["msg"] = "server error"
            return return_json

        if not transaction_executor.commit():
            return_json["msg"] = "SQL Insert error"
            return return_json

        return_json["success"] = 1
        return_json["token"] = make_jwt_token(email)

    return return_json


@user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    return_json = {"success": 0, "msg": "", "token": "", "isAdmin": 0}

    validator = Validator()
    validator.required([email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    with TransactionExecutor() as transaction_executor:
        """
        Check whether email exists in database and get salt, password  and isAdmin
        """
        success_flag, result = transaction_executor.query_sql(
            "SELECT salt, password, isAdmin from Users WHERE email = %(email)s",
            {"email": email},
            fetch_one=True,
        )
        if success_flag:
            if result == None:
                return_json["msg"] = "Email doesn't exist"
                return return_json
        else:
            return_json["msg"] = "Server error"
            return return_json

        salt, password_in_database, is_admin = result
        hash_password = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode(), 100000
        ).hex()

        if hash_password != password_in_database:
            return_json["msg"] = "Password is wrong"
            return return_json

        if not transaction_executor.commit():
            return_json["msg"] = "SQL Insert error"
            return return_json

        return_json["success"] = 1
        return_json["token"] = make_jwt_token(email, is_admin="1" if is_admin else "0")

        if is_admin:
            return_json["isAdmin"] = 1

    return return_json
