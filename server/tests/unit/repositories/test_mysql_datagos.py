import unittest

from server.domain.trace.datagos_trace import DatagosTrace
from server.infrastructure.persistence import get_mysql_client
from server.infrastructure.persistence import MySqlDatagosRepository


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
