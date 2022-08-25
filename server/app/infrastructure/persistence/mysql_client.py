from typing import Optional, Iterable, Any, List, Dict

import pymysql
import pymysql.cursors


class MySqlClient:
    def __init__(
        self,
        host: str,
        user: str,
        port: str,
        passwd: str,
        database: Optional[str] = None,
    ):
        self._connection = pymysql.Connection(
            host=host,
            port=int(port),
            user=user,
            password=passwd,
            db=database,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def cursor(self):
        return self._connection.cursor()

    def fetchall(
        self, query: str, args: Optional[Iterable[Any]] = None
    ) -> List[Dict[str, Any]]:

        self._connection.ping()  # reconnecting mysql
        with self._connection.cursor() as cursor:
            cursor.execute(query, args)

            res = list(cursor)

        return res

    def insert(self, query: str, args: Optional[Iterable[Any]] = None):
        try:
            with self.cursor() as cursor:
                cursor.execute(query, args)
            # connection is not autocommit by default. So you must commit to save changes.
            self._connection.commit()

        finally:
            self._connection.close()

    def close(self):
        if self._connection:
            self._connection.close()


def get_mysql_client() -> MySqlClient:
    return MySqlClient(host="127.0.0.1",
                       port="8306",
                       user="root",
                       passwd="datagos",
                       database="datagos"
                       )
