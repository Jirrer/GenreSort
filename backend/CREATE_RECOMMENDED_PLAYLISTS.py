from spotipyMethods import getPlaylistTrackIds, getTrackGenres, createPlaylists, getApiCounter, clearApiCounter

#To DO: make every method type safe

def startCreate_Recommended_Playlists(sp, playlistID):
    trackIDs = getPlaylistTrackIds(playlistID, sp); print("Pulled Track Ids")
    trackGenres = getTrackGenres(trackIDs, sp); print("Pulled Genres")
    newPlaylists = generateNewPlaylists(trackGenres); print("Generated Playlists")
    createPlaylists(newPlaylists, sp); print("Created Playlists")

    print(f"Spotify API Calls: {getApiCounter}")
    clearApiCounter()

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