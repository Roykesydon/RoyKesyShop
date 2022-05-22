from multiprocessing import connection

import pymysql
from dbutils.pooled_db import PooledDB

import utils.connection_pool as connection_pool

from .config import get_config


class TransactionExecutor:
    def __enter__(self):
        self.connection = connection_pool.connection_pool.connection()
        return self

    def __exit__(self, type, value, traceback):
        if self.connection is not None:
            self.connection.close()

    def execute_sql(self, sql_query, params):
        success_flag = True
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query, params)

        except Exception as error:
            print("Execute sql failed: {}".format(error))
            success_flag = False
            self.connection.rollback()

        finally:
            return success_flag

    def query_sql(self, sql_query, params, fetch_one=False):
        success_flag = True
        return_data = None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query, params)

                if fetch_one:
                    return_data = cursor.fetchone()
                else:
                    return_data = cursor.fetchall()

        except Exception as error:
            print("Query failed: {}".format(error))
            self.connection.rollback()
            success_flag = False

        return success_flag, return_data

    def commit(self):
        success_flag = True
        try:
            self.connection.commit()
        except Exception as error:
            print("Commit failed: {}".format(error))
            self.connection.rollback()
            success_flag = False
        finally:
            return success_flag
