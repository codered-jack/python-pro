from bs4 import BeautifulSoup
import requests

MOVIES_URL = (
    "https://web.archive.org/web/20200518073855/"
    "https://www.empireonline.com/movies/features/best-movies-2/"
)
OUTPUT_FILE = "movies.txt"


def fetch_movies_page(url):
    """Fetch the HTML source for the Empire top movies page.

    Example:
    html = fetch_movies_page(MOVIES_URL)
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_movie_titles(html):
    """Extract movie titles from Empire HTML.

    Example output (first few before reverse):
    ["100) Stand By Me", "99) Raging Bull", ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    movie_titles = soup.find_all(name="h3", class_="title")
    titles = [title.getText() for title in movie_titles]
    titles.reverse()  # Make list ascending from 1 to 100.
    return titles


def save_titles(titles, file_path):
    """Write one movie title per line.

    Example line:
    1) The Godfather
    """
    with open(file_path, "w", encoding="utf-8") as file:
        for title in titles:
            file.write(f"{title}\n")


def main():
    movies_page = fetch_movies_page(MOVIES_URL)
    titles = parse_movie_titles(movies_page)
    print(titles)
    save_titles(titles, OUTPUT_FILE)


if __name__ == "__main__":
    main()
