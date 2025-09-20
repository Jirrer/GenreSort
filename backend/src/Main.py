import os, spotipy, APICounter
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
from PullGenres import getTrackGenres
from ParseUserPlaylist import getUserTracks
from CreatePlaylists import createPlaylists

userPlaylist = "16VvnG7Zv0HPykw4mom76K"
numberOfPlaylist = 3 # Plus one for misc

# some artists dont have genres
# What I want to do - create folder 
#   in that folder have a playlist for each category (maybe max 3)
#   and a playlist for those without genres

def main():
    load_dotenv()

    sp = getSp(True)

    global userPlaylist
    trackIDs = getUserTracks(userPlaylist, sp); print("Pulled Track Ids")
    trackGenres = getTrackGenres(trackIDs, sp); print("Pulled Genres")
    newPlaylists = generateNewPlaylists(trackGenres); print("Generated Playlists")
    createPlaylists(newPlaylists, sp); print("Created Playlists")
    
def getSp(elevatedAuth):
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    if (elevatedAuth):
        REDIRECT_URI = "http://localhost:8888/callback" 
        SCOPE = "playlist-modify-public playlist-modify-private"

        sp_oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            show_dialog=True
        )

        auth_url = sp_oauth.get_authorize_url()
        print("Go to this URL in your browser:")
        print(auth_url)

        redirect_response = input("\nPaste the full redirect URL here: ").strip()

        code = sp_oauth.parse_response_code(redirect_response)
        access_token = sp_oauth.get_access_token(code, as_dict=False)  

        return spotipy.Spotify(auth=access_token)
    
    else:
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

if __name__ == "__main__": 
    main()
    print(f"Spotify API Calls: {APICounter.numApiCalls}")