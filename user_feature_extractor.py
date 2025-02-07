from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
import json

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
spotify = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=120)


#  reading in tracks.json
with open("data\\users\\227whclz22iewgm7htfoxxfoa_tracks.json") as tracks:
    tracks_list = json.load(tracks)

#  get the URIs of all the songs in the tracks_list
uri_list = []

print("Extracting track URIs from list")

for i, track in enumerate(tracks_list):
    uri = tracks_list[i]["uri"]
    uri_list.append(uri)

print(f"Extraction completed: {len(uri_list)} total tracks ")


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

print("Audio feature extraction process START")

while True:

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
            print(f"Track {i + start} is unavailable")

    if end >= len(uri_list):
        print("Audio feature extraction process END")
        break

    end += 100
    start = end - 100

#  writing the results to a json file
audio_features_json = json.dumps(audio_feature_list)

with open("data\\users\\227whclz22iewgm7htfoxxfoa_features.json", "a") as tracks:
    tracks.write(audio_features_json)
