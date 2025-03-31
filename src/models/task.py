from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    name: str
    description: str
    due_date: datetime
    completed: bool = False 