import datetime
import json

from server.app.domain.repositories.DatagosInteface import DatagosRepository
from server.app.infrastructure.persistence.mysql_client import MySqlClient


class MySqlDatagosRepository(DatagosRepository):

    def __init__(self, db_client: MySqlClient):
        self._db_client = db_client

    def find_all(self):
        sql_query = "SELECT * FROM traces"
        return self._db_client.fetchall(query=sql_query)
        pass

    def save(self, trace: dict, trace_type:str, service_name:str):
        sql_query = """
                INSERT INTO traces (trace, trace_type, service_name)
                     VALUES (%s, %s, %s)
        """

        args = (trace, trace_type, service_name, datetime.datetime.now())
        args = (trace, trace_type, service_name)
        self._db_client.insert(query=sql_query, args=args)
        pass
