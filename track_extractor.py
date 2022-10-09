from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
import json
import time

#  calling spotify api keys from local drive
api_path = f'{os.getenv("API")}\\spotify.json'

with open(api_path) as api:
    key = json.load(api)

client_id = key["data102"]["client_id"]
client_secret = key["data102"]["client_secret"]


# configuring Spotify client credentials
auth_manager = SpotifyClientCredentials(client_id=client_id,
                                        client_secret=client_secret,
                                        requests_timeout=10
                                        )
spotify = spotipy.Spotify(auth_manager=auth_manager)


#  TODO: if we want to increase number of playlist extracted, we can manually collect usernames and extract their playlists

#  10k long playlists as default
#  will add more playlist URIs
playlists_uri = ["spotify:playlist:5S8SJdl1BDc0ugpkEvFsIL",
                "spotify:playlist:6yPiKpy7evrwvZodByKvM9"
                ]

playlists = spotify.user_playlists('spotify')

#  extracting playlists from Spotify
print("Adding playlist URIs from Spotify")

while playlists:
    for playlist in playlists['items']:
        playlists_uri.append(playlist['uri'])
    if playlists['next']:
        playlists = spotify.next(playlists)
    else:
        playlists = None
        print(f"Extraction completed: {len(playlists_uri)} playlists")

#  list of extracted songs
tracks_list = []

def extract_track(index) -> dict:
    """This extracts the essential features from each track from the playlist. 

    Args:
        index (int): index of the specific track from the playlist

    Returns:
        dict: relevant features from each track
    """
    track_features_dict = {}
    
    track = playlist["items"][index]["track"]
    
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
                         "uri"]
    
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
        
    return track_features_dict

#  go through all the playlists available
for i, playlist_uri in enumerate(playlists_uri):
    
    #  to get the title of the playlist
    playlist_name = spotify.playlist(playlist_id=playlist_uri, fields="name")["name"]
    
    print(f"Start playlist #{i} of {len(playlist_uri)}: {playlist_name}")
    
    #  go through all the pages of the playlist 
    offset = 0

    while True:
        playlist = spotify.playlist_items(playlist_id=playlist_uri, limit=100, offset=offset)
        items = playlist["items"]
        next = playlist["next"]
        
        for i, item in enumerate(items):
            tracks_list.append(extract_track(i))
            print(f"Track {i + offset}: {items[i]['track']['name']} is done")
            
        #  this ends the loop
        #  if there is no more next url then we've reached the end
        if next is None:
            break
        
        #  so that we can move on from the 100-song limit 
        offset += 100
        
        #  let the program rest
        time.sleep(5)
    
    print(f"End: {playlist_name}")

print(f"Extraction process completed: {len(tracks_list)} total tracks")

#  writing the results to a json file
tracks_json = json.dumps(tracks_list)

with open("data\\tracks.json", "a") as tracks:
    tracks.write(tracks_json)