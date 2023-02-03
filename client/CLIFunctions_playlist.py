import Spotify_Client as scv1
import Spotify_Client_V2 as scv2


class CLIFunctions:
    client_version = None
    sc = None
    
    def __init__(self, client_version=''):
        self.client_version = client_version
        if self.client_version == 'v1':
            s

    
    def url_parse (self, url=None):
        if (url == None):
            raise Exception("Incorrect/null argument")
        