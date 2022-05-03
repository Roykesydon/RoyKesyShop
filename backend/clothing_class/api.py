import base64
from cmath import cos
from fileinput import filename
from pathlib import Path

from flask import Blueprint, request

from utils.jwt_handle import check_jwt_token_and_get_info
from utils.transaction_executor import TransactionExecutor
from utils.validator import Validator

clothingClass = Blueprint("clothing_class", __name__)

"""
Get all parent clothing classes with their sub classes
"""


@clothingClass.route("/", methods=["GET"])
def get_all_classes():
    returnJson = {"success": 0, "msg": "", "data": None}

    with TransactionExecutor() as transactionExecutor:
        successFlag, result = transactionExecutor.query_sql(
            "SELECT class, subClass from ClothingClass",
            {},
        )
    if not successFlag:
        returnJson["msg"] = "Can't get data"
        return returnJson

    classDict = {}

    for [parentClass, subClass] in result:
        try:
            classDict[parentClass].append(subClass)
        except:
            classDict[parentClass] = [subClass]

    returnJson["success"] = 1
    returnJson["data"] = classDict
    return returnJson


"""
Get clothing with chosen parent class.
Get a batch of clothing every time by the batch index.
"""


@clothingClass.route("/<string:parentClass>", methods=["GET"])
def get_clothing_with_parent_class():
    pass
    # batch = request.args.get("batch", default=0, type=int)
    # BATCH_SIZE = 20
    # returnJson = {"success": 0, "msg": "", "data": None}
    # with TransactionExecutor() as transactionExecutor:
    #     successFlag, result = transactionExecutor.query_sql(
    #         "SELECT _ID, title, cost, imageExtension, sizes from Clothing WHERE isDeleted = false order by _ID DESC limit %(BATCH_SIZE)s offset %(offset)s",
    #         {"BATCH_SIZE": BATCH_SIZE, "offset": batch * BATCH_SIZE},
    #     )
    # if not successFlag:
    #     returnJson["msg"] = "Can't get data"
    #     return returnJson

    # returnJson["success"] = 1
    # returnJson["data"] = result
    # return returnJson


"""
Get clothing with chosen parent class and sub class.
Get a batch of clothing every time by the batch index.
"""


@clothingClass.route("/<string:parenClass>/<string:subClass>", methods=["GET"])
def get_clothing_with_sub_class(filename):
    pass
    # if Path(f"./uploadFiles/clothingImages/{filename}").is_file():
    #     return send_from_directory(
    #         "./uploadFiles/clothingImages/", f"{filename}"
    #     )
    # return "Can't find file"


@clothingClass.route("/", methods=["POST"])
def create_clothing_class():
    data = request.get_json()

    parentClass = data["parentClass"]
    subClass = data["subClass"]

    token = request.headers.get("Authorization").replace("Bearer ", "")

    returnJson = {"success": 0, "msg": ""}

    """
    Check jwt token and get info of it
    """
    tokenParseResult = check_jwt_token_and_get_info(token, checkIsAdmin=True)

    if not tokenParseResult["success"]:
        returnJson["msg"] = tokenParseResult["msg"]
        return returnJson

    """
    Check input format
    """
    validator = Validator()
    validator.required([parentClass, subClass])
    validator.check_clothing_parent_class(parentClass)
    validator.check_clothing_sub_class(subClass)
    errors = validator.get_errors()

    if len(errors) != 0:
        returnJson["msg"] = errors[0]
        return returnJson

    """
    Insert Clothing class to database
    """
    with TransactionExecutor() as transactionExecutor:
        """
        Check whether class composition have already been used
        """
        successFlag, result = transactionExecutor.query_sql(
            "SELECT * from ClothingClass WHERE binary class = %(class)s and binary subClass = %(subClass)s",
            {"class": parentClass, "subClass": subClass},
            fetchOne=True,
        )

        if successFlag:
            if result != None:
                returnJson["msg"] = "Class composition already been used"
                return returnJson
        else:
            returnJson["msg"] = "server error"
            return returnJson

        insertString = "INSERT INTO ClothingClass(class, subClass) \
            values (%(class)s, %(subClass)s)"
        successFlag = transactionExecutor.execute_sql(
            insertString,
            {
                "class": parentClass,
                "subClass": subClass,
            },
        )
        if not successFlag:
            returnJson["msg"] = "Server error"
            return returnJson

        if not transactionExecutor.commit():
            returnJson["msg"] = "SQL Insert error"
            return returnJson

    returnJson["success"] = 1
    return returnJson
