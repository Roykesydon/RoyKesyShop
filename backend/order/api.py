import base64
from ast import keyword
from cmath import cos
from fileinput import filename
from pathlib import Path

from flask import Blueprint, request, send_from_directory

from utils.jwt_handle import check_jwt_token_and_get_info, make_jwt_token
from utils.transaction_executor import TransactionExecutor
from utils.validator import Validator

order = Blueprint("order", __name__)


@order.route("/", methods=["GET"])
def get_all_order():
    """
    Admin can use this API to get recent record of order information
    """
    recent_count = request.args.get("recent_count", default=500, type=int)


@order.route("/with_email", methods=["POST"])
def get_order_own_by_email():
    """
    Get particular user's order information
    """
    data = request.get_json()

    token = request.headers.get("Authorization").replace("Bearer ", "")
    order_email = ""
    recent_count = 100

    if "email" in data.keys():
        order_email = data["email"]

    if "recentCount" in data.keys():
        recent_count = int(data["recentCount"])

    """
    Check jwt token and get email of it
    """
    token_parse_result = check_jwt_token_and_get_info(token)
    if not token_parse_result["success"]:
        return_json["msg"] = token_parse_result["msg"]
        return return_json

    if token_parse_result["info"]["isAdmin"] != "1":
        order_email = token_parse_result["info"]["email"]

    return_json = {"success": 0, "msg": "", "data": None}

    """
    Check input format
    """
    validator = Validator()
    validator.required([order_email])
    validator.check_email(order_email)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    with TransactionExecutor() as transaction_executor:
        success_flag, result = transaction_executor.query_sql(
            "SELECT _ID, cost, name, address, phone, status, isDeleted, clothingID, size, count FROM \
                (SELECT _ID, email, cost, name, address, phone, status, isDeleted FROM Orders order by _ID DESC limit %(recent_count)s) as TopOrders INNER JOIN OrderClothingDetail\
                 ON TopOrders._ID = OrderClothingDetail.orderID WHERE email = %(email)s order by _ID DESC",
            {"recent_count": recent_count, "email": order_email},
        )
        if not success_flag:
            return_json["msg"] = "Can't get data"
            return return_json

        # print(result[:3])
        # print()
        orders = []
        previous_order_id = None
        for i in range(len(result)):
            clothing = (
                str(result[i][7]) + "-" + str(result[i][8]) + "-" + str(result[i][9])
            )

            if result[i][0] == previous_order_id:
                orders[-1]["clothing"] += "," + clothing
                continue

            previous_order_id = result[i][0]

            orders.append(
                {
                    "order_id": result[i][0],
                    "cost": result[i][1],
                    "name": result[i][2],
                    "address": result[i][3],
                    "phone": result[i][4],
                    "status": result[i][5],
                    "isDeleted": result[i][6],
                    "clothing": clothing,
                }
            )

    return_json["success"] = 1
    return_json["data"] = orders
    return return_json


@order.route("/", methods=["POST"])
def create_order():
    data = request.get_json()
    token = request.headers.get("Authorization").replace("Bearer ", "")

    return_json = {"success": 0, "msg": ""}

    """
    Check jwt token and get info of it
    """
    token_parse_result = check_jwt_token_and_get_info(token)

    if not token_parse_result["success"]:
        return_json["msg"] = token_parse_result["msg"]
        return return_json

    name = data["name"]
    address = data["address"]
    phone_number = data["phoneNumber"]
    clothing = data["clothing"]
    email = token_parse_result["info"]["email"]

    """
    Check input format
    """
    validator = Validator()
    validator.required([name, address, phone_number, clothing, email])
    validator.check_name(name)
    validator.check_address(address)
    validator.check_phone(phone_number)
    validator.check_clothing(clothing)
    validator.check_email(email)
    errors = validator.get_errors()

    if len(errors) != 0:
        return_json["msg"] = errors[0]
        return return_json

    with TransactionExecutor() as transaction_executor:
        """
        Calculate order's total cost
        """
        total_cost = 0
        clothing = clothing.split(",")
        for item in clothing:
            clothing_id, size, count = tuple(item.split("-"))

            """
            get cost of single clothing with above clothing_id
            """
            success_flag, result = transaction_executor.query_sql(
                "SELECT cost from Clothing WHERE _ID = %(clothing_id)s",
                {"clothing_id": clothing_id},
                fetch_one=True,
            )

            if success_flag:
                if result == None:
                    return_json["msg"] = f"Can't find clothing with ID: {clothing_id}"
                    return return_json

                cost = float(result[0])
                total_cost += cost * float(count)

            else:
                return_json["msg"] = "server error"
                return return_json

        """
        Insert Order to database and store in folder
        """
        insertString = "INSERT INTO Orders(cost, email, name, address, phone) \
            values (%(cost)s, %(email)s, %(name)s, %(address)s, %(phone)s)"
        success_flag = transaction_executor.execute_sql(
            insertString,
            {
                "cost": total_cost,
                "email": email,
                "name": name,
                "address": address,
                "phone": phone_number,
            },
        )
        if not success_flag:
            return_json["msg"] = "Server error"
            return return_json

        """
        Get the new insert Order _ID
        """
        success_flag, result = transaction_executor.query_sql(
            "select LAST_INSERT_ID()",
            {},
            fetch_one=True,
        )

        order_id = result[0]

        for item in clothing:
            clothing_id, size, count = tuple(item.split("-"))
            """
            Insert Order's related clothing detail to database
            """
            insertString = "INSERT INTO OrderClothingDetail(orderID, clothingID, size, count) \
                values (%(order_id)s, %(clothing_id)s, %(size)s, %(count)s)"
            success_flag = transaction_executor.execute_sql(
                insertString,
                {
                    "order_id": order_id,
                    "clothing_id": clothing_id,
                    "size": size,
                    "count": count,
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
