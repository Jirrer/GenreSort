import os, spotipy, APICounter, webbrowser, threading
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

auth_code = None
auth_event = threading.Event()

@app.route("/passInPlaylist", methods=["POST"])
def recievePlaylist():
    data = request.json
    playlistID = data.get("message", "")
    print(playlistID)

    if validPlaylistId(playlistID): runPlaylistCreation(playlistID); return jsonify({"status": "success"})
    else: return jsonify({"status": "Invalid Playlist ID"})

@app.route("/callback")
def callback():
    global auth_code
    auth_code = request.args.get("code")
    auth_event.set()
    return "Successfully authenticated\nYou can close this this tab\nYou may need to refresh spotify to see changes"

def validPlaylistId(data):
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    try:
        playlist = sp.playlist(data) # test if I need that variable
        return True
    
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        return False

def runPlaylistCreation(userPlaylist):
    global elavatedSpotifyAuth
    sp = getSp(True)

    trackIDs = getUserTracks(userPlaylist, sp); print("Pulled Track Ids")
    trackGenres = getTrackGenres(trackIDs, sp); print("Pulled Genres")
    newPlaylists = generateNewPlaylists(trackGenres); print("Generated Playlists")
    createPlaylists(newPlaylists, sp); print("Created Playlists")

    print(f"Spotify API Calls: {APICounter.numApiCalls}")
    
def getSp(elevatedAuth):
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    if (elevatedAuth): # Elevated perms
        REDIRECT_URI = os.getenv("REDIRECT_URI")
        SCOPE = "playlist-modify-public playlist-modify-private"

        sp_oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            show_dialog=True
        )

        auth_url = sp_oauth.get_authorize_url() 
        webbrowser.open(auth_url)

        print("Waiting for Spotify auth...")
        auth_event.wait()  # blocks here until /callback sets the code

        access_token = sp_oauth.get_access_token(auth_code, as_dict=False)
        return spotipy.Spotify(auth=access_token)

    else: # Regular perms
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