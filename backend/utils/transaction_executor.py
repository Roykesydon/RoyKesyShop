from multiprocessing import connection

import pymysql

from .config import get_config


class TransactionExecutor:
    def __enter__(self):
        config = get_config()
        self.connection = pymysql.connect(
            host=str(config["db"]["host"]),
            user=str(config["db"]["user"]),
            password=str(config["db"]["password"]),
            db=str(config["db"]["database"]),
            charset="utf8",
            autocommit=False,
        )
        return self

    def __exit__(self, type, value, traceback):
        if self.connection is not None:
            self.connection.close()

    def execute_sql(self, sqlQuery, params):
        successFlag = True
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sqlQuery, params)

        except Exception as error:
            print("Execute sql failed: {}".format(error))
            successFlag = False
            self.connection.rollback()

        finally:
            return successFlag

    def query_sql(self, sqlQuery, params, fetchOne=False):
        successFlag = True
        returnData = None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sqlQuery, params)

                if fetchOne:
                    returnData = cursor.fetchone()
                else:
                    returnData = cursor.fetchall()

        except Exception as error:
            print("Query failed: {}".format(error))
            self.connection.rollback()
            successFlag = False

        return successFlag, returnData

    def commit(self):
        successFlag = True
        try:
            self.connection.commit()
        except Exception as error:
            print("Commit failed: {}".format(error))
            self.connection.rollback()
            successFlag = False
        finally:
            return successFlag
