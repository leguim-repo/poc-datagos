from abc import ABC, abstractmethod

from domain.trace.datagos_trace import DatagosTrace


class DatagosRepository(ABC):

    @abstractmethod
    def save(self, trace: DatagosTrace):
        pass

    @abstractmethod
    def find_all(self):
        pass
