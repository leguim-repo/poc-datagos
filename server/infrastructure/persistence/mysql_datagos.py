import json

from server.domain.repositories.DatagosInteface import DatagosRepository
from server.domain.trace.datagos_trace import DatagosTrace
from server.infrastructure.persistence.mysql_client import MySqlClient


class MySqlDatagosRepository(DatagosRepository):

    def __init__(self, db_client: MySqlClient):
        self._db_client = db_client

    def find_all(self):
        sql_query = "SELECT * FROM traces"
        return self._db_client.fetchall(query=sql_query)
        pass

    def save(self, trace: DatagosTrace):
        sql_query = """
                INSERT INTO traces (trace, trace_type, service_name)
                     VALUES (%s, %s, %s)
        """

        args = (json.dumps(trace.trace), trace.type, trace.service_name)
        self._db_client.insert(query=sql_query, args=args)
