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

# configuring Spotify client credentials + to get current user data
auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri="http://localhost:8888/callback",
                            scope=scope,
                            requests_timeout=10
                            )

spotify = spotipy.Spotify(auth_manager=auth_manager)

#  retrieving top 50 most played songs of user
user_top_tracks = spotify.current_user_top_tracks(limit=50, offset=0, time_range="long_term")["items"]

#  list of tracks + features in dictionary form
tracks_list = []

#  get features of each track in the top 50
for i, track in enumerate(user_top_tracks):
    
    track_features_dict = {}
    
    song_title = track["name"]
    artist_name = track["artists"][0]["name"]
    album_title = track["album"]["name"] 
    release_date = track["album"]["release_date"]
    duration = track["duration_ms"]
    popularity =  track["popularity"]
    uri = track["uri"]
    
    song_features_keys = ["song_title",
                         "artist_name",
                         "album_title",
                         "release_date",
                         "duration",
                         "popularity",
                         "uri"
                         ]
    
    song_features_values = [song_title,
                            artist_name,
                            album_title,
                            release_date,
                            duration,
                            popularity,
                            uri
                            ]
    
    for feat_key, feat_values in zip(song_features_keys, song_features_values):
        track_features_dict[feat_key] = feat_values
        
    tracks_list.append(track_features_dict)

#  get username
user_name = spotify.current_user()["id"]

#  convert current tracks_list to json format
#  write extracted tracks to json for each user
tracks_json = json.dumps(tracks_list)

with open(f"data\\users\\{user_name}_tracks.json", "w") as tracks:
    tracks.write(tracks_json)

