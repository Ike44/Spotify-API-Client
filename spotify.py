import requests



auth_url = "https://accounts.spotify.com/authorize"
token_data = {
    'response_type' : 'code',
    'redirect_uri' : 'http://localhost:3000/',
    'state' : 56,
    'scope' : 'playlist-read-private playlist-read-collaborative'
    }



response = requests.get(auth_url, params=token_data)
print(response.history[0].url)