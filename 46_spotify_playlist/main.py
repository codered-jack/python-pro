from bs4 import BeautifulSoup
import requests
from spotify import create_billboard_playlist

BILLBOARD_BASE_URL = "https://www.billboard.com/charts/hot-100"


def fetch_billboard_html(year_to_travel):
    """Fetch Billboard Hot 100 page HTML for a given date.

    Example:
    fetch_billboard_html("2005-03-20")
    """
    billboard_url = f"{BILLBOARD_BASE_URL}/{year_to_travel}/"
    response = requests.get(billboard_url)
    response.raise_for_status()
    return response.text


def parse_song_titles(html):
    """Extract and clean song titles from Billboard HTML.

    Example output:
    ["We Belong Together", "Hollaback Girl", ...]
    """
    soup = BeautifulSoup(html, "html.parser")
    song_titles = soup.select(selector="li h3.c-title")
    song_list = [song.getText().strip() for song in song_titles]
    # Remove empty rows and keep readable titles only.
    return [song for song in song_list if song]


def main():
    year_to_travel = input(
        "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
    ).strip()
    songs_page = fetch_billboard_html(year_to_travel)
    all_songs = parse_song_titles(songs_page)
    print(all_songs)

    # Create a private Spotify playlist with the fetched songs.
    # Example playlist name: "2005-03-20 Billboard 100"
    playlist_id = create_billboard_playlist(year_to_travel, all_songs)
    print(f"Created/updated playlist: {playlist_id}")


if __name__ == "__main__":
    main()
