import base64
from ast import keyword
from cmath import cos
from fileinput import filename
from pathlib import Path

from flask import Blueprint, request, send_from_directory

from utils.jwt_handle import check_jwt_token_and_get_info, make_jwt_token
from utils.transaction_executor import TransactionExecutor
from utils.validator import Validator

clothing = Blueprint("clothing", __name__)

"""
Get clothing info without detail.
Get a batch of clothing every time by the batch index.
"""


@clothing.route("/", methods=["GET"])
def index():
    batch = request.args.get("batch", default=0, type=int)
    BATCH_SIZE = 20
    return_json = {"success": 0, "msg": "", "data": None}
    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT _ID, title, cost, imageExtension, sizes from Clothing WHERE isDeleted = false order by _ID DESC limit %(BATCH_SIZE)s offset %(offset)s",
            {"BATCH_SIZE": BATCH_SIZE, "offset": batch * BATCH_SIZE},
        )
    if not success_flag:
        return_json["msg"] = "Can't get data"
        return return_json

    return_json["success"] = 1
    return_json["data"] = result
    return return_json

@clothing.route("/<int:id>", methods=["GET"])
def get_clothing_by_id():
    return_json = {"success": 0, "msg": "", "data": None}
    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT _ID, title, cost, imageExtension, sizes from Clothing WHERE isDeleted = false and _ID = %(clohting_id)s",
            {"clothing_id": id},
        )
    if not success_flag:
        return_json["msg"] = "Can't get data"
        return return_json

    return_json["success"] = 1
    return_json["data"] = result
    return return_json

@clothing.route("/search/<string:keyword>", methods=["GET"])
def search_by_keyword(keyword):
    """
    TODO: multiple keywords
    """
    batch = request.args.get("batch", default=0, type=int)
    BATCH_SIZE = 20

    return_json = {"success": 0, "msg": "", "data": None}
    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT _ID, title, cost, imageExtension, sizes from Clothing WHERE isDeleted = false and title LIKE CONCAT('%%', %(keyword)s, '%%') order by _ID DESC limit %(BATCH_SIZE)s offset %(offset)s",
            {
                "keyword": str(keyword),
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


@clothing.route("/image/<string:filename>", methods=["GET"])
def get_clothing_with_id(filename):
    if Path(f"./uploadFiles/clothingImages/{filename}").is_file():
        return send_from_directory("./uploadFiles/clothingImages/", f"{filename}")
    return "Can't find file"


@clothing.route("/", methods=["POST"])
def create_clothing():
    data = request.get_json()

    title = data["title"]
    cost = data["cost"]
    description = data["description"]
    selected_size = ",".join(data["selectedSize"])
    select_parent_class = data["selectParentClass"]
    select_sub_class = data["selectSubClass"]
    image = data["image"]
    token = request.headers.get("Authorization").replace("Bearer ", "")
    extension = image.split(";")[0].split("/")[-1]

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
    validator.required([title, cost, selected_size, image])
    validator.check_clothing_title(title)
    validator.check_clothing_cost(cost)
    validator.check_selected_size(selected_size)
    validator.check_upload_picture(image, extension)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    """
    Insert Clothing to database and store in folder
    """
    with TransactionExecutor() as transaction_executor:
        insertString = "INSERT INTO Clothing(title, description, cost, imageExtension, sizes, class, subClass) \
            values (%(title)s, %(description)s, %(cost)s, %(image_extension)s, %(sizes)s, %(class)s, %(sub_class)s)"
        success_flag = transaction_executor.execute_sql(
            insertString,
            {
                "title": title,
                "description": description,
                "cost": cost,
                "image_extension": extension,
                "sizes": selected_size,
                "class": select_parent_class,
                "sub_class": select_sub_class,
            },
        )
        if not success_flag:
            return_json["msg"] = "Server error"
            return return_json

        """
        Get the new insert clothing _ID
        """
        success_flag, result = transaction_executor.query_sql(
            "select LAST_INSERT_ID()",
            {},
            fetch_one=True,
        )

        if not success_flag:
            return_json["msg"] = "server error"
            return return_json

        clothing_id = result[0]

        """
        Save upload image
        """
        try:
            image_bytes = image.split(",")[-1]
            with open(
                "./uploadFiles/clothingImages/" + str(clothing_id) + "." + extension,
                "wb",
            ) as file:
                file.write(base64.b64decode(image_bytes))
        except:
            return_json["msg"] = "Save image fail"
            return return_json

        if not transaction_executor.commit():
            return_json["msg"] = "SQL Insert error"
            return return_json

    return_json["success"] = 1
    return return_json
