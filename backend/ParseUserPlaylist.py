import time, APICounter
from spotipy.exceptions import SpotifyException

#To-Do split up funciton

def getUserTracks(playlistID, sp):
    track_ids = set()
    
    try:
        results = sp.playlist_items(playlistID, additional_types=['track'])
        APICounter.numApiCalls += 1

    except SpotifyException as e:
        if e.http_status == 429:
            wait_time = int(e.headers.get("Retry-After", 5))
            print(f"Rate limited! Waiting {wait_time}s...")
            time.sleep(wait_time)
            results = sp.playlist_items(playlistID, additional_types=['track'])
            APICounter.numApiCalls += 1

        else:
            raise

    for item in results['items']:
        if item['track'] and item['track']['id']:
            track_ids.add(item['track']['id'])

    while results['next']:
        try:
            results = sp.next(results)
            APICounter.numApiCalls += 1

        except SpotifyException as e:
            if e.http_status == 429:
                wait_time = int(e.headers.get("Retry-After", 5))
                print(f"Rate limited! Waiting {wait_time}s...")
                time.sleep(wait_time)
                APICounter.numApiCalls += 1
                continue
    
            else:
                raise

        for item in results['items']:
            if item['track'] and item['track']['id']:
                track_ids.add(item['track']['id'])

    return list(track_ids)
