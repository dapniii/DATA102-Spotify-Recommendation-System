from email.mime import audio
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
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret, requests_timeout=10
)
spotify = spotipy.Spotify(auth_manager=auth_manager)


#  reading in tracks.json
with open("tracks.json") as tracks:
    tracks_list = json.load(tracks)

#  get the URIs of all the songs in the tracks_list
uri_list = []

for i, track in enumerate(tracks_list):
    uri = tracks_list[i]["uri"]
    uri_list.append(uri)


def audio_feat_extractor(index) -> dict:
    """Extracts the audio features from each track.

    Args:
        index (int): index of the specific track from the list to
        be extracted from.

    Returns:
        dict: complete dictionary of extracted data from each track.
    """
    audio_feature_dict = {}

    track_instance = extracted_af_list[index]

    audio_features = [
        "uri",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "time_signature",
    ]

    #  extract data feature by feature
    for feature in audio_features:
        audio_feature_dict[feature] = track_instance[feature]

    return audio_feature_dict


#  list of audio features for each track
audio_feature_list = []

end = 100
start = 0

while end != 10100:     #  TODO: improve loop condition so that it would be scalable

    time.sleep(5)

    #  per 100 batches of uri
    trunc_list = uri_list[start:end]

    #  retrieving data through the api
    extracted_af_list = spotify.audio_features(trunc_list)

    for i, instance in enumerate(extracted_af_list):
        try:
            uri_ref = extracted_af_list[i]["uri"]
            audio_feature_list.append(audio_feat_extractor(i))
            print(f"Track {i + start}: {uri_ref} is done")
        except TypeError:
            audio_feature_list.append(None)
            print(f"Track {i + start} is unavailable")

    end += 100
    start = end - 100

#  writing the results to a json file
audio_features_json = json.dumps(audio_feature_list)

with open("audio_features.json", "w") as tracks:
    tracks.write(audio_features_json)
