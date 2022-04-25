import time

import jwt

from utils.config import get_config


def make_jwt_token(email, isAdmin="0"):
    config = get_config()
    return jwt.encode(
        {"email": email, "isAdmin": isAdmin, "exp": time.time() + 60 * 60 * 24 * 3},
        config["jwt_secret_key"],
        algorithm="HS256",
    )


def check_jwt_token_and_get_info(token, checkIsAdmin=False):
    config = get_config()

    returnInfo = {
        "success": False,
        "msg": "",
        "info": {},
    }

    """
    Check token integrity
    """
    try:
        info = jwt.decode(
            token,
            config["jwt_secret_key"],
            algorithms=["HS256"],
        )
    except:
        returnInfo["msg"] = "Can't decode token"
        return returnInfo

    """
    Check token timeliness
    """
    if time.time() > info["exp"]:
        returnInfo["msg"] = "Token have expired"
        return returnInfo

    if checkIsAdmin:
        """
        Check token authority
        """
        if info["isAdmin"] != "1":
            returnInfo["msg"] = "Permission denied"
            return returnInfo

    returnInfo["success"] = True
    returnInfo["info"] = info
    return returnInfo
