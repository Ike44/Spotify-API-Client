# Spotify-API-Client
This is a Spotify API client I created that has the ability to automatically refresh tokens and comes with robust search functionality. It comes with 2 versions: **version 1 (../client/Spotify_Client.py)** uses the client credentials flow auth process from spotify's API and **version 2 (../client/Spotify_Client_V2.py)** uses the Authentication Code flow auth process from spotify's API.

*Purpose:* In my spotify account, I have a huge playlist of over 2,000 songs because I could not be bothered to create smaller playlists for different purposes and that is generally how I like to listen to music, but there came multiple times when I wanted to listen to songs from a particular artist; I could do this by simply playing songs on the artists' profile but I only wanted to listen to songs from that artist that I liked (which would be the ones in my playlist), and there the idea was born. I could have used other spotify API client's like spotipy but I wanted to build one for myself so I would use it for my particular functionality and build to my liking as well as make it modular enough to where I can build additional features on top of it whenever I wanted to do so.

The project is equipped with a command line interface (CLI) which is how the interaction with user playlist functionality is implemented.
Instructions for use are on the way!

*There are a lot of features that will be built onto this project but this is the initial main feature. I am certainly open to new ideas and ways for implementation so feel free to hit me up with any suggestions.*

## SETUP
* First thing you need to do is to create a `congig.env` that contains the environment variables (Spotify client id and client secret from your spotify app on developer.spotify.com). Follow the same format in the `configEnvSample.txt` file to create your env file.
* You will need to install the latest version of python https://realpython.com/installing-python/ 
* You will also need to install pip: https://pip.pypa.io/en/stable/installation/
* `cd` into the project directory.
* Use pip to install pipenv : `pip install pipenv`
* Run the command: `pipenv shell`
* You will need to install the following modules: 
  * python-dotenv: `pipenv install python-dotenv`
  * python requests: `pipenv install requests`

## Running the program
To run the program (playlist feature), navigate to the /client directory and run the `PlaylistFeatureCLI.py` file (`../client/PlaylistFeatureCLI.py`) in the terminal and follow the instructions carefully.
