import os, spotipy, uuid, threading
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from spotipyMethods import getElivatedSP, validPlaylistId
from CREATE_RECOMMENDED_PLAYLISTS import startCreate_Recommended_Playlists

load_dotenv()

numberOfPlaylist = 3 # Plus one for misc

app = Flask(__name__, static_folder="dist", static_url_path="/")

@app.route("/")
@app.route("/<path:path>")
def serve_react(path=""):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

auth_code = None
auth_event = threading.Event()
temp_playlist_map = {}

@app.route("/pingServer")
def pingServer():
    return jsonify({"status": "success"})

@app.route("/passinNewPlaylists", methods=["POST"]) #change name
def runCreate_Recommended_Playlists():
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

    startCreate_Recommended_Playlists(sp, playlistID)

    return "Successfully authenticated! You can close this tab."


if __name__ == "__main__": 
    app.run(debug=True)