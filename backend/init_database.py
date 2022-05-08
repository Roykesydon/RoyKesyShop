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

cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
connection.commit()
cursor.execute("DROP TABLE IF EXISTS Users;")
connection.commit()
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
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


cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
connection.commit()
cursor.execute("DROP TABLE IF EXISTS ClothingClass;")
connection.commit()
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
connection.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS ClothingClass( \
    class varchar(30) NOT NULL,\
    subClass varchar(30) NOT NULL,\
    PRIMARY KEY (class, subClass) );"
)
connection.commit()


cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
connection.commit()
cursor.execute("DROP TABLE IF EXISTS Clothing;")
connection.commit()
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
connection.commit()


cursor.execute(
    "CREATE TABLE IF NOT EXISTS Clothing( \
    _ID int(8) NOT NULL AUTO_INCREMENT, \
    title varchar(50) NOT NULL,\
    description varchar(505),\
    cost varchar(15) NOT NULL, \
    imageExtension varchar(10) NOT NULL,\
    isDeleted bool DEFAULT FALSE,\
    sizes varchar(50) NOT NULL, \
    class varchar(30) NOT NULL,\
    subClass varchar(30) NOT NULL,\
    PRIMARY KEY (_ID),\
    FOREIGN KEY clothingClassForeignKey (class, subClass) REFERENCES ClothingClass(class, subClass));"
)
connection.commit()


cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
connection.commit()
cursor.execute("DROP TABLE IF EXISTS Orders;")
connection.commit()
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
connection.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS Orders( \
    _ID int(8) NOT NULL AUTO_INCREMENT, \
    cost varchar(50) NOT NULL,\
    email varchar(50) NOT NULL, \
    name varchar(40) NOT NULL, \
    address varchar(100) NOT NULL,\
    phone varchar(20) NOT NULL,\
    status varchar(20) DEFAULT ('wait pay'),\
    isDeleted bool DEFAULT FALSE,\
    PRIMARY KEY (_ID),\
    FOREIGN KEY OrdersAndUserForeignKey (email) REFERENCES Users(email));"
)
connection.commit()


cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
connection.commit()
cursor.execute("DROP TABLE IF EXISTS OrderClothingDetail;")
connection.commit()
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
connection.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS OrderClothingDetail( \
    orderID int(8) NOT NULL,\
    clothingID int(8) NOT NULL,\
    size varchar(10),\
    count int(8) NOT NULL,\
    PRIMARY KEY (orderID, clothingID, size),\
    FOREIGN KEY ClothingForeignKey (clothingID) REFERENCES Clothing(_ID),\
    FOREIGN KEY OrderForeignKey (orderID) REFERENCES Orders(_ID));"
)
connection.commit()


cursor.close()
connection.close()
