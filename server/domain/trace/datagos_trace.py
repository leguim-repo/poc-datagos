from dataclasses import dataclass


@dataclass(frozen=True)
class DatagosTrace:
    trace: dict
    type: str
    service_name: str
