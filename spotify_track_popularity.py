import requests
import base64
import json
from operator import itemgetter
from tabulate import tabulate

def get_spotify_token(client_id, client_secret):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_artist_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']

def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&limit=50"
    headers = get_auth_header(token)
    albums = []
    while url:
        result = requests.get(url, headers=headers)
        json_result = json.loads(result.content)
        albums.extend(json_result['items'])
        url = json_result.get('next')
    return albums

def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    tracks = []
    while url:
        result = requests.get(url, headers=headers)
        json_result = json.loads(result.content)
        tracks.extend(json_result['items'])
        url = json_result.get('next')
    return tracks

def get_tracks_popularity(token, track_ids):
    url = "https://api.spotify.com/v1/tracks"
    headers = get_auth_header(token)
    all_tracks = []
    
    for i in range(0, len(track_ids), 50):  # Spotify allows up to 50 IDs per request
        batch = track_ids[i:i+50]
        params = {"ids": ",".join(batch)}
        result = requests.get(url, headers=headers, params=params)
        json_result = json.loads(result.content)
        all_tracks.extend(json_result['tracks'])
    
    return {track['id']: track['popularity'] for track in all_tracks if track}

def get_all_artist_tracks(token, artist_id):
    albums = get_artist_albums(token, artist_id)
    all_tracks = []
    track_ids = []
    for album in albums:
        album_tracks = get_album_tracks(token, album['id'])
        for track in album_tracks:
            if artist_id in [artist['id'] for artist in track['artists']]:
                all_tracks.append(track)
                track_ids.append(track['id'])
    popularity_dict = get_tracks_popularity(token, track_ids)
    for track in all_tracks:
        track['popularity'] = popularity_dict.get(track['id'], 0)
    return all_tracks

def sort_tracks_by_popularity(artist_id, token):
    tracks = get_all_artist_tracks(token, artist_id)
    sorted_tracks = sorted(tracks, key=itemgetter('popularity'), reverse=True)
    return sorted_tracks

def main():
    print("Spotify Track Popularity Application")
    print("====================================")
    
    client_id = input("Enter your Spotify Client ID: ")
    client_secret = input("Enter your Spotify Client Secret: ")
    artist_id = input("Enter the Spotify Artist ID: ")
    
    print("\nFetching data from Spotify...")
    token = get_spotify_token(client_id, client_secret)
    sorted_tracks = sort_tracks_by_popularity(artist_id, token)
    
    table_data = []
    for i, track in enumerate(sorted_tracks, 1):
        table_data.append([
            i,
            track['name'],
            track['popularity'],
            track['external_urls']['spotify']
        ])
    
    headers = ["#", "Track Name", "Popularity Score", "Spotify URL"]
    print("\nTracks sorted by popularity:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()