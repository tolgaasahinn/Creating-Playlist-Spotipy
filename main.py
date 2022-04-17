import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

Token = os.environ.get("TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "https://example.com"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",

)
)

date = input("Which year do you want to travel to ? type date in this format YYYY - MM - DD: ")
year = date.split("-")[0]
month = date.split("-")[1]
day = date.split("-")[2]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}")
top_hot = response.text

soup = BeautifulSoup(top_hot, "html.parser")
song_name = soup.find_all(name="h3", class_="a-no-trucate")
song_name_list = [name.getText().replace("\n", "") for name in song_name]
song_names = [name.replace('\t', "") for name in song_name_list]
artist_name = soup.find_all(name="span", class_="a-no-trucate")
artist_name_list = [name.getText().replace("\n", "") for name in artist_name]
artist_names = [name.replace('\t', "") for name in artist_name_list]

playlist_name = f"Track :BilBoard 100  Year: {date}"
user_id = sp.current_user()["id"]

SONG_URI_LIST = []
for i in range(100):
    result = sp.search(q=f"track:{song_names[i]} artist:{artist_names[i]}", type="track,artist")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        SONG_URI_LIST.append(uri)
    except IndexError:
        print(f"{song_names[i]} doesn't exist in Spotify. Skipped.")

create_playlist = sp.user_playlist_create(
    user=user_id,
    name=playlist_name,
    public=False,
)
sp.playlist_add_items(playlist_id=create_playlist["id"], items=SONG_URI_LIST)
