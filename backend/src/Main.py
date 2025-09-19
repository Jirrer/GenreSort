import os, spotipy, APICounter
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
from PullGenres import getTrackGenres
from ParseUserPlaylist import getUserTracks

userPlaylist = "6ldPqoCFrK5X75Bwp1B2uS"

# some artists dont have genres
# What I want to do - create folder 
#   in that folder have a playlist for each category (maybe max 3)
#   and a playlist for those without genres

def main():
    load_dotenv()

    sp = getSp(False)

    global userPlaylist
    trackIDs = getUserTracks(userPlaylist, sp)
    
    trackGenres = getTrackGenres(trackIDs, sp)

    print(f"Spotify API Calls: {APICounter.numApiCalls}")
    
    for key, value in trackGenres.items():
        print(f"track: {key}, genres: {value}")


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

if __name__ == "__main__":
    main()
