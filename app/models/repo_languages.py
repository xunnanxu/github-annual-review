from dataclasses import dataclass, field
from typing import Dict

@dataclass
class RepoLanguages:
    repo: str
    languages: Dict[str, int]
    language_scores: Dict[str, float] = field(init=False)

    def __post_init__(self):
        self.language_scores = {}
        total_bytes = 0
        for v in self.languages.values():
            total_bytes += v
        for k, v in self.languages.items():
            self.language_scores[k] = v / total_bytes

    def __hash__(self):
        return hash(self.repo)

    def __eq__(self, other):
        if not isinstance(other, RepoLanguages):
            return False
        return self.repo == other.repo