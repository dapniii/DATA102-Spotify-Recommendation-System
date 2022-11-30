import spotipy
import os
import json

from spotipy.oauth2 import SpotifyOAuth

#  calling spotify api keys from local drive
api_path = f'{os.getenv("API")}\\spotify.json'

with open(api_path) as api:
    key = json.load(api)

client_id = key["data102"]["client_id"]
client_secret = key["data102"]["client_secret"]

#  scope set to user-top-read
scope = "user-top-read"

# configuring Spotify client credentials
auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri="http://localhost:8888/callback",
                            username="aexylian",
                            scope=scope,
                            requests_timeout=10
                            )

spotify = spotipy.Spotify(auth_manager=auth_manager)

user_top_tracks = spotify.current_user_top_tracks(limit=1, offset=0, time_range="short_term")["items"][0]
print(user_top_tracks["name"])