import time
from itertools import islice
from spotipy.exceptions import SpotifyException

def getTrackGenres(trackstrs, sp):
    trackIDs = getTrackIDs(trackstrs, sp)
    output = {}
    cache = {}
    allAristIDs = getUniqueArtists(trackIDs)

    for batch in chunks(list(allAristIDs), 50):
        artists_info = safe_artists_fetch(sp, batch)
        
        for artist in artists_info:
            cache[artist["id"]] = artist["genres"]

    for track in trackIDs:
        if "track" in track: track = track["track"]

        genres = set()
        for artist in track["artists"]:
            genres.update(cache.get(artist["id"], []))

        output[track["id"]] = ",".join(genres)

    return output

def getTrackIDs(strs, sp):
    output = []
    for batch in chunks(strs, 50):
        info = sp.tracks(batch)["tracks"]
        output.extend(info)

    return output

def getUniqueArtists(trackList):
    output = set()

    for track in trackList:
        if "track" in track: track = track["track"]

        for artist in track["artists"]: output.add(artist["id"])

    return output 

def chunks(lst, n):
    for i in range(0, len(lst), n): yield lst[i:i + n]

def safe_artists_fetch(sp, artist_ids):
    while True:
        try:
            return sp.artists(artist_ids)["artists"]
        
        except SpotifyException as e:
            if e.http_status == 429: 
                wait_time = int(e.headers.get("Retry-After", 5))
                print(f"Rate limited! Waiting {wait_time}s...")
                time.sleep(wait_time)

            else:
                raise