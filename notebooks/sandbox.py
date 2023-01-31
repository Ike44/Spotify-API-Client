from Spotify_Client_V2 import*
import os
from dotenv import load_dotenv

load_dotenv("./config.env")
client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")

spotify_client = sc.SpotifyAPI(client_id, client_secret)
