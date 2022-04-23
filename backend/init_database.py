import pymysql
import yaml

with open("config.yml", "r") as f:
    cfg = yaml.safe_load(f)

connection = pymysql.connect(
    host=str(cfg["db"]["host"]),
    user=str(cfg["db"]["user"]),
    password=str(cfg["db"]["password"]),
    db=str(cfg["db"]["database"]),
    charset="utf8",
)


cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS Users;")
connection.commit()


cursor.execute(
    "CREATE TABLE IF NOT EXISTS Users( \
    name varchar(50),\
    email varchar(50) NOT NULL,\
    salt varchar(50) NOT NULL, \
    isAdmin bool DEFAULT FALSE,\
    password varchar(64) NOT NULL, \
    PRIMARY KEY (email) );"
)
connection.commit()

cursor.close()
connection.close()
