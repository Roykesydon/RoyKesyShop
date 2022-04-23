from multiprocessing import connection

import pymysql

from .config import get_config


class SQLExecutor:
    def _get_connection(self):
        config = get_config()
        connection = pymysql.connect(
            host=str(config["db"]["host"]),
            user=str(config["db"]["user"]),
            password=str(config["db"]["password"]),
            db=str(config["db"]["database"]),
            charset="utf8",
            autocommit=False,
        )
        return connection

    def execute_transaction(self, sqlQuerysAndParams):
        successFlag = True
        try:
            connection = self._get_connection()

            with connection.cursor() as cursor:
                for sqlQuery, params in sqlQuerysAndParams:
                    cursor.execute(sqlQuery, params)

            connection.commit()

        except Exception as error:
            print("Transaction failed: {}".format(error))
            successFlag = False
            connection.rollback()

        finally:
            connection.close()
            return successFlag

    def query_sql(self, sqlQuery, params, fetchOne=False):
        successFlag = True
        connection = None
        returnData = None

        try:
            connection = self._get_connection()

            with connection.cursor() as cursor:
                cursor.execute(sqlQuery, params)
                connection.commit()
                if fetchOne:
                    returnData = cursor.fetchone()
                else:
                    returnData = cursor.fetchall()

        except Exception as error:
            print("Query failed: {}".format(error))
            connection.rollback()
            successFlag = False

        finally:
            if connection is not None:
                connection.close()

        return successFlag, returnData
