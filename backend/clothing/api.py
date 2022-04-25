import base64
import hashlib
from cmath import cos

from flask import Blueprint, request

from utils.jwt_handle import check_jwt_token_and_get_info, make_jwt_token
from utils.transaction_executor import TransactionExecutor
from utils.validator import Validator

clothing = Blueprint("clothing", __name__)


@clothing.route("/", methods=["GET"])
def index():
    return "Hello clothing"


@clothing.route("/<int:id>", methods=["GET"])
def get_clothing_with_id(id):
    return "Hello clothing" + str(id)


@clothing.route("/", methods=["POST"])
def create_clothing():
    data = request.get_json()

    title = data["title"]
    cost = data["cost"]
    description = data["description"]
    selectedSize = ",".join(data["selectedSize"])
    image = data["image"]
    token = request.headers.get("Authorization").replace("Bearer ", "")
    extension = image.split(";")[0].split("/")[-1]

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
    validator.required([title, cost, selectedSize, image])
    validator.check_clothing_title(title)
    validator.check_clothing_cost(cost)
    validator.check_selected_size(selectedSize)
    validator.check_upload_picture(image, extension)
    errors = validator.get_errors()

    if len(errors) != 0:
        returnJson["msg"] = errors[0]
        return returnJson

    """
    Insert Clothing to database and store in folder
    """
    with TransactionExecutor() as transactionExecutor:
        insertString = "INSERT INTO Clothing(title, description, cost, imageExtension, sizes) \
            values (%(title)s, %(description)s, %(cost)s, %(imageExtension)s, %(sizes)s)"
        successFlag = transactionExecutor.execute_sql(
            insertString,
            {
                "title": title,
                "description": description,
                "cost": cost,
                "imageExtension": extension,
                "sizes": selectedSize,
            },
        )
        if not successFlag:
            returnJson["msg"] = "Server error"
            return returnJson

        """
        Get the new insert clothing _ID
        """
        successFlag, result = transactionExecutor.query_sql(
            "select LAST_INSERT_ID()",
            {},
            fetchOne=True,
        )

        if not successFlag:
            returnJson["msg"] = "server error"
            return returnJson

        clothingId = result[0]

        """
        Save upload image
        """
        try:
            imageBytes = image.split(",")[-1]
            with open(
                "./uploadFiles/clothingImages/" + str(clothingId) + "." + extension,
                "wb",
            ) as file:
                file.write(base64.b64decode(imageBytes))
        except:
            returnJson["msg"] = "Save image fail"
            return returnJson

        if not transactionExecutor.commit():
            returnJson["msg"] = "SQL Insert error"
            return returnJson

    returnJson["success"] = 1
    return returnJson
