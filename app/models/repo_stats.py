from dataclasses import dataclass
from datetime import datetime

from . import RepoLanguages

@dataclass
class RepoStats(RepoLanguages):
    created_at: datetime
    stars: int
    forks: int
    score: float

    def __hash__(self):
        return super.__hash__(self)

    def __eq__(self, other):
        return super.__eq__(self, other)