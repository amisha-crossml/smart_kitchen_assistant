from pytube import Search
from crewai.tools import tool
from contextlib import suppress

@tool("search video")
def search_youtube_links(query: str, limit: int = 5) -> str:
    """
    Search video on YouTube and return a list of video links as a string.

    Args:
        query (str): Video search prompt.
        limit (int, optional): Number of video links to return. Defaults to 5.

    Returns:
        str: Comma-separated YouTube video links.
    """
    with suppress(Exception):  # suppress logging errors from pytube
        search = Search(query)
    video_links = []
    for video in search.results:
        try:
            url = video.watch_url
            if "shorts" not in url:  # optionally skip Shorts
                video_links.append(url)
            if len(video_links) >= limit:
                break
        except Exception:
            continue  # in case any individual video breaks
    link =  ', '.join(video_links)
    return link
