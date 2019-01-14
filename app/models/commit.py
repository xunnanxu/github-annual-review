from dataclasses import dataclass, field

from .entity import Entity

@dataclass
class Commit(Entity):
    lines_added: int
    lines_deleted: int
    total: int = field(init=False)

    def __post_init__(self):
        self.total = self.lines_added + self.lines_deleted