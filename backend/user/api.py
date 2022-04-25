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

    returnJson = {"success": 0, "msg": "", "token": ""}

    validator = Validator()
    validator.required([email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        returnJson["msg"] = errors[0]
        return returnJson

    with TransactionExecutor() as transactionExecutor:
        """
        Check whether email already been used or not
        """
        successFlag, result = transactionExecutor.query_sql(
            "SELECT * from Users WHERE email = %(email)s",
            {"email": email},
            fetchOne=True,
        )

        if successFlag:
            if result != None:
                returnJson["msg"] = "Email already been used"
                return returnJson
        else:
            returnJson["msg"] = "server error"
            return returnJson

        """
        Insert user information into database
        """
        salt = os.urandom(16)
        salt = base64.b64encode(salt)

        hashPassword = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 100000
        ).hex()

        insertString = "INSERT INTO Users(name, email, salt, password) values (%(Name)s, %(email)s, %(salt)s, %(password)s)"
        successFlag = transactionExecutor.execute_sql(
            insertString,
            {
                "Name": None,
                "email": email,
                "salt": salt,
                "password": hashPassword,
            },
        )
        if not successFlag:
            returnJson["msg"] = "server error"
            return returnJson

        if not transactionExecutor.commit():
            returnJson["msg"] = "SQL Insert error"
            return returnJson

        returnJson["success"] = 1
        returnJson["token"] = make_jwt_token(email)

    return returnJson


@user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    returnJson = {"success": 0, "msg": "", "token": "", "isAdmin": 0}

    validator = Validator()
    validator.required([email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        returnJson["msg"] = errors[0]
        return returnJson

    with TransactionExecutor() as transactionExecutor:
        """
        Check whether email exists in database and get salt, password  and isAdmin
        """
        successFlag, result = transactionExecutor.query_sql(
            "SELECT salt, password, isAdmin from Users WHERE email = %(email)s",
            {"email": email},
            fetchOne=True,
        )
        if successFlag:
            if result == None:
                returnJson["msg"] = "Email doesn't exist"
                return returnJson
        else:
            returnJson["msg"] = "Server error"
            return returnJson

        salt, passwordInDatabase, isAdmin = result
        hashPassword = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode(), 100000
        ).hex()

        if hashPassword != passwordInDatabase:
            returnJson["msg"] = "Password is wrong"
            return returnJson

        if not transactionExecutor.commit():
            returnJson["msg"] = "SQL Insert error"
            return returnJson

        returnJson["success"] = 1
        returnJson["token"] = make_jwt_token(email, isAdmin="1" if isAdmin else "0")

        if isAdmin:
            returnJson["isAdmin"] = 1

    return returnJson
