import datetime
import unittest

from server.app.domain.trace.datagos_trace import DatagosTrace
from server.app.infrastructure.persistence.mysql_client import get_mysql_client
from server.app.infrastructure.persistence.mysql_datagos import MySqlDatagosRepository


class TestMySqlDatagosShould(unittest.TestCase):
    def test_save_trace(self):
        datagos_repo = MySqlDatagosRepository(db_client=get_mysql_client())
        self.assertIsNotNone(datagos_repo)

        trace_mock = DatagosTrace(trace={"message": "blabla", "method":"method_name"},
                                  type="test",
                                  service_name="mein_service",
                                  created_at=None)
        datagos_repo.save(trace=trace_mock)
        rows = datagos_repo.find_all()
        expected = []
        self.assertEqual(expected, rows)
