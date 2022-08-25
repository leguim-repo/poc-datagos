import json
import unittest

from server.app.infrastructure.persistence.mysql_client import get_mysql_client
from server.app.infrastructure.persistence.mysql_datagos import MySqlDatagosRepository


class TestMySqlDatagosShould(unittest.TestCase):
    def test_save_trace(self):
        datagos_repo = MySqlDatagosRepository(db_client=get_mysql_client())
        self.assertIsNotNone(datagos_repo)

        datagos_repo.save(trace=json.dumps({"value": "blabla"}),
                          trace_type="test",
                          service_name="mein_service")
        rows = datagos_repo.find_all()
        expected = []
        self.assertEqual(expected, rows)
