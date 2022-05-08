import base64
from cmath import cos
from fileinput import filename
from pathlib import Path

from flask import Blueprint, request

from utils.jwt_handle import check_jwt_token_and_get_info
from utils.transaction_executor import TransactionExecutor
from utils.validator import Validator

clothing_class = Blueprint("clothing_class", __name__)


@clothing_class.route("/", methods=["GET"])
def get_all_classes():
    """
    Get all parent clothing classes with their sub classes
    """
    return_json = {"success": 0, "msg": "", "data": None}

    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT class, subClass from ClothingClass",
            {},
        )
    if not success_flag:
        return_json["msg"] = "Can't get data"
        return return_json

    class_dict = {}

    for [parent_class, sub_class] in result:
        try:
            class_dict[parent_class].append(sub_class)
        except:
            class_dict[parent_class] = [sub_class]

    return_json["success"] = 1
    return_json["data"] = class_dict
    return return_json


@clothing_class.route("/<string:parent_class>", methods=["GET"])
def get_clothing_with_parent_class(parent_class):
    """
    Get clothing with chosen parent class.
    Get a batch of clothing every time by the batch index.
    """
    batch = request.args.get("batch", default=0, type=int)
    BATCH_SIZE = 20
    return_json = {"success": 0, "msg": "", "data": None}
    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT _ID, title, cost, imageExtension, sizes from Clothing WHERE isDeleted = false and class = %(parent_class)s order by _ID DESC limit %(BATCH_SIZE)s offset %(offset)s",
            {
                "parent_class": parent_class,
                "BATCH_SIZE": BATCH_SIZE,
                "offset": batch * BATCH_SIZE,
            },
        )
    if not success_flag:
        return_json["msg"] = "Can't get data"
        return return_json

    return_json["success"] = 1
    return_json["data"] = result
    return return_json


@clothing_class.route("/<string:parent_class>/<string:sub_class>", methods=["GET"])
def get_clothing_with_sub_class(parent_class, sub_class):
    """
    Get clothing with chosen parent class and sub class.
    Get a batch of clothing every time by the batch index.
    """
    batch = request.args.get("batch", default=0, type=int)
    BATCH_SIZE = 20
    return_json = {"success": 0, "msg": "", "data": None}
    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT _ID, title, cost, imageExtension, sizes from Clothing WHERE isDeleted = false and class = %(parent_class)s and subClass = %(sub_class)s order by _ID DESC limit %(BATCH_SIZE)s offset %(offset)s",
            {
                "parent_class": parent_class,
                "sub_class": sub_class,
                "BATCH_SIZE": BATCH_SIZE,
                "offset": batch * BATCH_SIZE,
            },
        )
    if not success_flag:
        return_json["msg"] = "Can't get data"
        return return_json

    return_json["success"] = 1
    return_json["data"] = result
    return return_json


@clothing_class.route("/", methods=["POST"])
def create_clothing_class():
    data = request.get_json()

    parent_class = data["parentClass"]
    sub_class = data["subClass"]

    token = request.headers.get("Authorization").replace("Bearer ", "")

    return_json = {"success": 0, "msg": ""}

    """
    Check jwt token and get info of it
    """
    token_parse_result = check_jwt_token_and_get_info(token, check_is_admin=True)

    if not token_parse_result["success"]:
        return_json["msg"] = token_parse_result["msg"]
        return return_json

    """
    Check input format
    """
    validator = Validator()
    validator.required([parent_class, sub_class])
    validator.check_clothing_parent_class(parent_class)
    validator.check_clothing_sub_class(sub_class)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    """
    Insert Clothing class to database
    """
    with TransactionExecutor() as transaction_executor:
        """
        Check whether class composition have already been used
        """
        success_flag, result = transaction_executor.query_sql(
            "SELECT * from ClothingClass WHERE binary class = %(class)s and binary subClass = %(sub_class)s",
            {"class": parent_class, "sub_class": sub_class},
            fetch_one=True,
        )

        if success_flag:
            if result != None:
                return_json["msg"] = "Class composition already been used"
                return return_json
        else:
            return_json["msg"] = "server error"
            return return_json

        insertString = "INSERT INTO ClothingClass(class, subClass) \
            values (%(class)s, %(sub_class)s)"
        success_flag = transaction_executor.execute_sql(
            insertString,
            {
                "class": parent_class,
                "sub_class": sub_class,
            },
        )
        if not success_flag:
            return_json["msg"] = "Server error"
            return return_json

        if not transaction_executor.commit():
            return_json["msg"] = "SQL Insert error"
            return return_json

    return_json["success"] = 1
    return return_json
