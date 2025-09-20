import os, spotipy, APICounter
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv
from PullGenres import getTrackGenres
from ParseUserPlaylist import getUserTracks
from CreatePlaylists import createPlaylists
from flask import Flask, request, jsonify

# To-Do: refactor all python code
# To-Do: work on algo to decide playlists
# To-Do: could make it so it adds to prexisting playlists 

load_dotenv()

numberOfPlaylist = 3 # Plus one for misc
elavatedSpotifyAuth = True

app = Flask(__name__)

@app.route("/passInPlaylist", methods=["POST"])
def recievePlaylist():
    data = request.json
    playlistID = data.get("message", "")
    print(playlistID)

    if validPlaylistId(playlistID): runPlaylistCreation(playlistID); return jsonify({"status": "success"})
    else: return jsonify({"status": "Invalid Playlist ID"})

def validPlaylistId(data):
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    try:
        playlist = sp.playlist(data)
        return True
    
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        return False

def runPlaylistCreation(userPlaylist):
    global elavatedSpotifyAuth
    sp = getSp(elavatedSpotifyAuth)

    trackIDs = getUserTracks(userPlaylist, sp); print("Pulled Track Ids")
    trackGenres = getTrackGenres(trackIDs, sp); print("Pulled Genres")
    newPlaylists = generateNewPlaylists(trackGenres); print("Generated Playlists")
    createPlaylists(newPlaylists, sp); print("Created Playlists")

    print(f"Spotify API Calls: {APICounter.numApiCalls}")
    
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
    app.run(debug=True)