from datetime import datetime
from itertools import islice
from spotipy.exceptions import SpotifyException
import APICounter

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