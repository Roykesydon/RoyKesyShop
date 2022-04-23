import base64
import hashlib
import os
import re

import jwt
import pymysql
from flask import Blueprint, request

from utils.config import get_config
from utils.sql_executor import SQLExecutor
from utils.validator import Validator

user = Blueprint("user", __name__)


@user.route("/")
def index():
    return "Hello user"


@user.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")

    returnJson = {"success": 0, "msg": "", "token": ""}

    validator = Validator()
    validator.required([email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        returnJson["msg"] = errors[0]
        return returnJson

    sqlExecutor = SQLExecutor()

    """
    Check whether email already been used or not
    """
    successFlag, result = sqlExecutor.query_sql(
        "SELECT * from Users WHERE email = %(email)s", {"email": email}, fetchOne=True
    )
    if successFlag:
        if result != None:
            returnJson["msg"] = "email already been used"
            return returnJson
    else:
        returnJson["msg"] = "server error"
        return returnJson


    """
    Insert user information into database
    """
    salt = os.urandom(16)
    salt = base64.b64encode(salt)

    hashPassword = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000).hex()


    insertString = "INSERT INTO Users(name, email, salt, password) values (%(Name)s, %(email)s, %(salt)s, %(password)s)"
    successFlag = sqlExecutor.execute_transaction(
        [
            (
                insertString,
                {
                    "Name": None,
                    "email": email,
                    "salt": salt,
                    "password": hashPassword,
                },
            )
        ]
    )
    if not successFlag:
        returnJson["msg"] = "server error"
        return returnJson

    config = get_config()

    returnJson["success"] = 1
    returnJson["token"] = jwt.encode(
        {"email": email}, config["jwt_secret_key"], algorithm="HS256"
    )
    return returnJson


@user.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    returnJson = {"success": 0, "msg": "", "token": ""}

    validator = Validator()
    validator.required([email, password])
    validator.check_email(email)
    validator.check_password(password)
    errors = validator.get_errors()

    if len(errors) != 0:
        returnJson["msg"] = errors[0]
        return returnJson

    sqlExecutor = SQLExecutor()

    """
    Check whether email exists in database and get salt and password 
    """
    successFlag, result = sqlExecutor.query_sql(
        "SELECT salt, password from Users WHERE email = %(email)s", {"email": email}, fetchOne=True
    )
    if successFlag:
        if result == None:
            returnJson["msg"] = "email doesn't exist"
            return returnJson
    else:
        returnJson["msg"] = "server error"
        return returnJson

    salt, passwordInDatabase = result
    hashPassword = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode(), 100000).hex()

    if hashPassword != passwordInDatabase:
        returnJson["msg"] = "password is wrong"
        return returnJson
        

    config = get_config()

    returnJson["success"] = 1
    returnJson["token"] = jwt.encode(
        {"email": email}, config["jwt_secret_key"], algorithm="HS256"
    )
    return returnJson