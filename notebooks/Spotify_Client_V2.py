#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install requests
#!pip install print-dict


# In[2]:


import base64
import datetime
from urllib.parse import urlencode
import requests as rq
import webbrowser
import os
#from print_dict import pd
#from dotenv import load_dotenv


# In[9]:


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    auth_url = "https://accounts.spotify.com/authorize"
    baseURL = 'https://api.spotify.com/v1'
    auth_code = None
    refresh_token = None
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.perform_login()
    
    def get_client_credentials(self):
        """
        Returns a base64 string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret.")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_auth_data(self):
        auth_data = {
            'client_id' : self.client_id,
            'response_type' : 'code',
            'redirect_uri' : 'http://localhost:3000/',
            'scope' : 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
            }
        return auth_data
    
    def perform_login(self):
        response = rq.get(self.auth_url, params=self.get_auth_data())
        if response.status_code not in range(200, 299):
            raise Exception("Could not login!")
        webbrowser.open(response.url)
    
    def parse_url_for_code(self, redirect_url=None):
        #parse URL for code
        if redirect_url == None:
            raise Exception("Invalid URL")
        response_url = redirect_url
        split_url = response_url.split('?')
        split_url = split_url[1].split('=')
        #print(split_url)
        auth_code1 = split_url[1]
        #return auth_code
        self.auth_code = auth_code1
        self.get_initial_access_token()
    
    def get_initial_token_data(self):
        token_data = {
            'grant_type' : "authorization_code",
            'code' : self.auth_code,
            'redirect_uri' : 'http://localhost:3000/',
            'client_id' : self.client_id,
            'client_secret': self.client_secret
        }
        return token_data
    
    def get_initial_access_token(self):
        auth_response = rq.post(url=self.token_url, data=self.get_initial_token_data())
        if auth_response.status_code not in range(200, 299):
            raise Exception("Could not get initial access token")
        s = auth_response.json()
        now = datetime.datetime.now()
        self.access_token = s['access_token']
        self.refresh_token = s['refresh_token']
        expires_in = s['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True 
    
    
    def get_refresh_token_data(self):
        refresh_data= {
            'grant_type':'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id' : self.client_id,
            'client_secret': self.client_secret
        }
        return refresh_data

    
    def perform_auth(self):
        token_url = self.token_url
        refresh_data = self.get_refresh_token_data()
        token_headers = self.get_token_headers()
        
        r = rq.post(url=token_url, data=refresh_data)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        data = r.json()
        now = datetime.datetime.now()
        refresh_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = refresh_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
       
        
    def get_resource(self, lookup_id, resource_type='albums',version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = rq.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
        
    def get_album(self, _id):
        return self.get_resource(_id, resource_type = 'albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type = 'artists')
    
    def base_search(self, query_params):
        access_token = self.get_access_token()
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = rq.get(lookup_url, headers = headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance (query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type" : search_type.lower()})
        print(query_params)
        # When doing the queries with operators match the query to the operator query in terms of type(artists, albums,etc.)
        return self.base_search(query_params)
        

#Playlist features

    def get_user_playlists(self, resource_type='users', version='v1', user_id='null', limit=50):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{user_id}/playlists"
        query_params = urlencode({'limit' : 50})
        final_endpoint = f"{endpoint}?{query_params}"
        headers = self.get_resource_header()
        r = rq.get(final_endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def get_next_page(self, url=None):
        if url == None:
            raise Exception("Invalid argument")
        headers = self.get_resource_header()
        r = rq.get(url, headers=headers)
        if r.status_code not in range(200,299):
            print(r.status_code)
            return {}
        return r.json()
    
    #this particular vairable/field is only needed for the list_user_playlists method
    user_playlists = []
    def list_user_playlists(self, response=None):
        if response == None:
            raise Exception("Invalid argument")
        #print(self.user_playlists)
        for item in response['items']:
            temp = {'name' : item['name'],
                    'id' : item['id'],
                   'uri' : item['uri']}
            self.user_playlists.append(temp)
        while(response['next'] != None):
            self.list_user_playlists(self.get_next_page(response['next']))
            break
        return self.user_playlists
    
    def clear_user_playlists(self):
        self.user_playlists = []
        
    def get_playlist_items(self, resource_type='playlists', version='v1', playlist_id='null', limit=100):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{playlist_id}/tracks"
        query_params = urlencode({'limit' : limit, 'fields': 'items(added_by.id,uri,track(name,artists(href,id,uri,name,spotify),id,uri,duration,explicit,href,album(name,id,uri))),href,limit,next,offset,previous,total'})
        final_endpoint = f"{endpoint}?{query_params}"
        #print(final_endpoint)
        headers = self.get_resource_header()
        r = rq.get(final_endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    
    #this particular vairable/field is only needed for the parse_playlists_items method
    playlist_items = []
    def parse_playlist_items(self, response=None):
        if response == None:
            raise Exception("Invalid argument")
        for item in response['items']:
            #pd(item)
            if item['track']==None:
                continue
            artists = []
            for i in item['track']['artists']:
                w = {'name' : i['name'],
                     'id' : i['id'],
                     'uri' : i['uri']
                    }
                artists.append(w)

            q = {'song_name' : item['track']['name'], 'id' : item['track']['id'],'uri' : item['track']['uri'],
                                          'artists' : artists }
            self.playlist_items.append(q)
        while(response['next'] != None):
            self.parse_playlist_items(self.get_next_page(response['next']))
            break
        return self.playlist_items

    def clear_playlist_items(self):
        self.playlist_items = []
        
        
    def create_playlist(self, resource_type='users', version='v1', user_id='null', 
                        name=None, description='', public=False, artist=None, playlist_name=None):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{user_id}/playlists"
        headers = self.get_resource_header()
        if name == None:
            name = f"{artist} : {playlist_name}"
            #print(name)
        post_data = {'name' : name,
                    'description' : description,
                    'public' : public}
        r = rq.post(endpoint, headers=headers, json=post_data)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    
    def get_spotify_uri(self, id=None, resource_type='artist'):
        #resource type example = artist,album,track
        if id == None:
            raise Exception("Invalid argument")
        uri = f"spotify:{resource_type}:{id}"
        return uri
    
    def add_song_to_playlist(self, resource_type='playlists', version='v1', uri_list=None, playlist_id=None):
        if uri_list == None or playlist_id == None:
            raise Exception("Invalid argument")
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{playlist_id}/tracks"
        headers = self.get_resource_header()
        post_data = {'uris' : uri_list}
        r = rq.post(endpoint, headers=headers, json=post_data)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    

