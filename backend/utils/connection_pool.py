import pymysql
from dbutils.pooled_db import PooledDB

from utils.config import get_config


def init():
    config = get_config()
    global connection_pool
    connection_pool = PooledDB(
        creator=pymysql,  # Modules using linked databases
        maxconnections=8,  # The maximum number of connections allowed in the connection pool, 0 and None indicate unlimited connections
        mincached=2,  # At least idle links created in the link pool during initialization, 0 means not to create
        maxcached=5,  # The most idle links in the link pool, 0 and None are unlimited
        maxshared=0,  # The maximum number of links shared in the link pool. 0 and None represent all shares. PS: useless, because the threadsafety of pymysql, MySQL dB and other modules is 1. No matter how many values are set, the "maxcached" is always 0, so all links are always shared.
        blocking=True,  # If there is no connection available in the connection pool, whether to block waiting. True, wait; False, do not wait and report an error
        maxusage=None,  # The maximum number of times a link can be reused, None means unlimited
        setsession=[],  # List of commands executed before starting a session. For example: ["set datestyle to...", "set time zone..."]
        ping=0,
        # ping MySQL Server, check whether the service is available.# For example: 0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host=str(config["db"]["host"]),
        port=3306,
        user=str(config["db"]["user"]),
        password=str(config["db"]["password"]),
        database=str(config["db"]["database"]),
        charset="utf8",
        autocommit=False,
    )
