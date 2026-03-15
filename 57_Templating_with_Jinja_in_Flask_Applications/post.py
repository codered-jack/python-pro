from dataclasses import dataclass


@dataclass
class Post:
    """Represents one blog post item from the API."""

    id: int
    title: str
    subtitle: str
    body: str
