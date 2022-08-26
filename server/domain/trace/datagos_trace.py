from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class DatagosTrace:
    trace: dict
    type: str
    service_name: str
    created_at: Optional[datetime]
