from abc import ABC, abstractmethod


class DatagosRepository(ABC):

    @abstractmethod
    def save(self, trace: dict, trace_type: str, service_name: str):
        pass

    @abstractmethod
    def find_all(self):
        pass
