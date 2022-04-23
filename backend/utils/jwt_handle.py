import time

import jwt

from utils.config import get_config


def make_jwt_token(email):
    config = get_config()
    return jwt.encode(
        {"email": email, "exp": time.time() + 60 * 60 * 24 * 3},
        config["jwt_secret_key"],
        algorithm="HS256",
    )
