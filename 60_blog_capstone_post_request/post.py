from dataclasses import dataclass


@dataclass
class Post:
    """Represents one blog post fetched from API."""

    id: int
    author: str
    date: str
    title: str
    subtitle: str
    image_url: str
    body: str
