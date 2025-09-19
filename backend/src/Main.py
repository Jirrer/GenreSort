import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv

def main():
    load_dotenv()

    sp = getSp(False)

    trackIDs = [sp.track('https://open.spotify.com/track/6wdIe1ep26qiaIaiHF5b9F'), 
                sp.track('https://open.spotify.com/track/5v6wvFBcvedd6olUk3r9J8'),
                sp.track('https://open.spotify.com/track/22bX2FwXSvG49G0bPWm5nc')
                ]
    
    trackGenres = getTrackGenres(trackIDs, sp)

    print(trackGenres)


def getSp(elevatedAuth):
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    if (elevatedAuth):
        REDIRECT_URI = "http://localhost:8888/callback"  # Must match Spotify dashboard
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
    
def getTrackGenres(trackIDS, sp):
    output = {}

    for track in trackIDS:
        songArtists = [artist['id'] for artist in track["artists"]]

        artists = sp.artists(songArtists)["artists"]

        genres = set()
        for artist in artists: 
            for genre in artist["genres"]: genres.add(genre) 

        output[track['id']] = ",".join(genres) 

    return output

if __name__ == "__main__":
    main()
