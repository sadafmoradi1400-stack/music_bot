import requests


def search_music(query, limit=5):
    url = "https://itunes.apple.com/search"
    params = {
        "term": query,
        "media": "music",
        "entity": "song",
        "limit": limit,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    results = data.get("results", [])
    if not results:
        return []

    songs = []
    for item in results:
        songs.append({
            "track_name": item.get("trackName"),
            "artist_name": item.get("artistName"),
            "album_name": item.get("collectionName"),
            "preview_url": item.get("previewUrl"),  
            "artwork_url": item.get("artworkUrl100"),
            "release_date": item.get("releaseDate", "")[:10],
        })

    return songs


if __name__ == "__main__":
    q = input("نام آهنگ یا خواننده را وارد کنید: ")
    result = search_music(q)
    if result is None:
        print("خطا در اتصال به API")
    elif not result:
        print("نتیجه‌ای یافت نشد")
    else:
        for s in result:
            print(f"{s['track_name']} - {s['artist_name']} | {s['preview_url']}")