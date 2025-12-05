import os, spotipy, uuid, threading, time
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from spotipy.exceptions import SpotifyException
from spotipy.exceptions import SpotifyException
from datetime import datetime
from spotipy.exceptions import SpotifyException

numberOfPlaylist = 3 # Plus one for misc

def createPlaylists(playlistDict, sp):
    currDate = datetime.now()

    for genere, songArray in playlistDict.items():
        playlistName = f"Sorted by {genere} - {currDate}"

        playlist = sp.user_playlist_create(
            user = sp.me()["id"],
            name = playlistName,
            public = False,
            description = ""
        )

        APICounter.numApiCalls += 2

        for index in range(0, len(songArray), 100):
            sp.playlist_add_items(playlist["id"], songArray[index:index+100])
            APICounter.numApiCalls += 1

def validPlaylistId(data):
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    try:
        sp.playlist(data) 
        return True
    
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        return False

def runNewPlaylistsCreation(sp, playlistID):
    trackIDs = getUserTracks(playlistID, sp); print("Pulled Track Ids")
    trackGenres = getTrackGenres(trackIDs, sp); print("Pulled Genres")
    newPlaylists = generateNewPlaylists(trackGenres); print("Generated Playlists")
    createPlaylists(newPlaylists, sp); print("Created Playlists")

    print(f"Spotify API Calls: {APICounter.numApiCalls}")
    
def getElivatedSP():
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    SCOPE = "playlist-modify-public playlist-modify-private"

    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )

    return sp_oauth

def getClientSP():
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    return spotipy.Spotify(auth_manager=auth_manager)

def generateNewPlaylists(trackDict):
    output = {'misc': []}
    genresCounts = getGenresCounts(trackDict.values())
    sortedGenreCount = sorted(genresCounts.items(), key=lambda item: item[1], reverse=True)

    global numberOfPlaylist
    allowedGenres = sortedGenreCount[:numberOfPlaylist]

    for genre in allowedGenres: output[genre[0]] = []

    for track, genresStr in trackDict.items():
        if not genresStr: output['misc'].append(track); continue

        songGenres = genresStr.split(',')

        for genreName in reversed(allowedGenres):
            if genreName[0] in songGenres: output[genreName[0]].append(track); break

    return output

def getGenresCounts(genreStr):
    output = {}

    for genreList in genreStr:
        for genre in genreList.split(','):
            if not genre: continue

            if genre in output: output[genre] += 1
            else: output[genre] = 1

    return output

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
            genres.update(cache.get(artist["id"], ["unknown"]))

        output[track["id"]] = ",".join(genres)

    return output

def getTrackIDs(strs, sp):
    output = []
    for batch in chunks(strs, 50):
        info = sp.tracks(batch)["tracks"]
        APICounter.numApiCalls += 1
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
            APICounter.numApiCalls += 1
            return sp.artists(artist_ids)["artists"]
        
        except SpotifyException as e:
            if e.http_status == 429: 
                wait_time = int(e.headers.get("Retry-After", 5))
                print(f"Rate limited! Waiting {wait_time}s...")
                time.sleep(wait_time)

            else:
                raise




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
