import requests
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube_playlist(query: str):
    """
    Search for a relevant YouTube playlist.
    Safe against network errors, quota issues, and missing API keys.
    """

    # If API key is missing, fail silently
    if not YOUTUBE_API_KEY:
        return None

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "playlist",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        data = response.json()
    except Exception:
        return None

    if "items" in data and data["items"]:
        item = data["items"][0]
        return {
            "title": item["snippet"]["title"],
            "url": f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
        }

    return None
