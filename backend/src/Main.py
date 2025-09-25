import os, spotipy, APICounter, uuid, threading
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv
from PullGenres import getTrackGenres
from ParseUserPlaylist import getUserTracks
from CreatePlaylists import createPlaylists
from flask import Flask, request, jsonify

# To-Do: change how auth opens browser (requres refactor)
# To-Do: work on algo to decide playlists
# To-Do: could make it so it adds to prexisting playlists 

load_dotenv()

numberOfPlaylist = 3 # Plus one for misc

app = Flask(__name__)

auth_code = None
auth_event = threading.Event()
temp_playlist_map = {}

@app.route("/pingServer")
def pingServer():
    return jsonify({"status": "success"})

@app.route("/passinNewPlaylists", methods=["POST"])
def passinNewPlaylists():
    data = request.json
    playlistID = data.get("message", "")

    if validPlaylistId(playlistID):
        token = str(uuid.uuid4())  # unique temporary token
        temp_playlist_map[token] = playlistID

        sp_oauth = getElivatedSP()
        auth_url = sp_oauth.get_authorize_url(state=token)

        print("Waiting for Spotify auth...")
        return jsonify({"status": "success", "auth_url": auth_url})
        
    else: return jsonify({"status": "Invalid Playlist ID"})

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state_token = request.args.get("state")
    playlistID = temp_playlist_map.pop(state_token, None)


    if not playlistID:
        return "No playlist found for this session or token expired."



    sp_oauth = getElivatedSP()          
    token = sp_oauth.get_access_token(code, as_dict=False)
    sp = spotipy.Spotify(auth=token)

    runNewPlaylistsCreation(sp, playlistID)

    return "Successfully authenticated! You can close this tab."

    

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
    print("good to go")

    # trackIDs = getUserTracks(auth_code, sp); print("Pulled Track Ids")
    # trackGenres = getTrackGenres(trackIDs, sp); print("Pulled Genres")
    # newPlaylists = generateNewPlaylists(trackGenres); print("Generated Playlists")
    # createPlaylists(newPlaylists, sp); print("Created Playlists")

    # print(f"Spotify API Calls: {APICounter.numApiCalls}")
    
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

if __name__ == "__main__": 
    app.run(debug=True)