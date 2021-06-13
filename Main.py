import requests
import os
from dotenv import load_dotenv
from time import time, sleep
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()
oauthtoken = os.getenv("OAUTH_TOKEN")
playlist = os.getenv("PLAYLIST_URI")
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
station_short = "SPGOLD"
next_station_short = "SPDNB"

def getSongName(): #Return List: ["Author", "Song"]
    aeg = int(time()-2)
    URL = "https://dad.akaver.com/api/SongTitles/SKYMEDIAALL?jsoncallback=jQuery3210868290125465718_1623506590480&_="+str(aeg)
    page = requests.get(URL).content.decode()
    author = page.split(station_short)[1].split(next_station_short)[0].split("0,")[1].split('"Artist":"')[1].split('"')[0]
    song =page.split(station_short)[1].split(next_station_short)[0].split("0,")[1].split('"Title":"')[1].split('"')[0]
    r = [author, song]
    return r

def findSongURI(songName): #Return String:"Spotify URI"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    songName = songName.split("%28")[0]
    
    try:
        result = str(sp.search(songName, limit=1, market="EE")).split("'spotify:track:")[1].split("'")[0]
    except IndexError:
        return 0
    return result

def addSongToPlaylist(uri): #Returns null
    

    sp2 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))
    sp2.playlist_add_items(playlist_id=playlist, items=[uri])
    return
while True:

    fail = open("uris.txt", "r+")
    uris = fail.readlines()
    spaget = getSongName()
    uri = findSongURI(str(spaget[0]) + " " + str(spaget[1]))
    if uri != 0:
        for j in range(len(uris)):
            uris[j] = uris[j].strip("\n")
        if uri not in uris:
            addSongToPlaylist(uri)
            fail.write(str(uri + "\n"))
        fail.close()
        sleep(5)
