import time

import jwt

from utils.config import get_config


def make_jwt_token(email, is_admin="0"):
    config = get_config()
    return jwt.encode(
        {"email": email, "isAdmin": is_admin, "exp": time.time() + 60 * 60 * 24 * 3},
        config["jwt_secret_key"],
        algorithm="HS256",
    )


def check_jwt_token_and_get_info(token, check_is_admin=False):
    config = get_config()

    return_info = {
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
        return_info["msg"] = "Can't decode token"
        return return_info

    """
    Check token timeliness
    """
    if time.time() > info["exp"]:
        return_info["msg"] = "Token have expired"
        return return_info

    if check_is_admin:
        """
        Check token authority
        """
        if info["isAdmin"] != "1":
            return_info["msg"] = "Permission denied"
            return return_info

    return_info["success"] = True
    return_info["info"] = info
    return return_info
