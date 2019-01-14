from dataclasses import dataclass

@dataclass
class Entity:
    message: str
    url: str
    repo: str