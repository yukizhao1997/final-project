
import unittest
import sqlite3
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = "207cc5dde4cc44d79564a3d7be32a14b"
secret = "763787b786144c41b138f51c172f41cd"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def setupPresentSpotifryTable(cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS now_Spotify_Data (present_id TEXT PRIMARY KEY,present_title TEXT, present_popularity INTEGER, present_artist TEXT,present_speechiness INTEGER,present_loudness INTEGER, present_instrumentalnes INTEGER)")
    cur.execute('SELECT now_name,now_singer FROM BillBoard')
    song_artist_list = cur.fetchall()
    
    song_list = []
    song_dict = []
    for i in range(len(song_artist_list)):
        song_list.append(song_artist_list[i][0])
    for m in song_list:
        content = sp.search(m,type="track")
        song_dict.append(content)
    
    
    spotify_songname_list=[]
    spotify_songpopu_list=[]
    sporify_songartist_list=[]
    spotify_songid_list = []
    
    for item in song_dict:
        for t in item['tracks']['items']:
            spotify_songname = t.get("name", "")
            spotify_songname_list.append(spotify_songname)
            
            spotify_songpopu = t.get("popularity", "")
            spotify_songpopu_list.append(spotify_songpopu)
            
            spotify_songid = t.get("id", "")
            spotify_songid_list.append(spotify_songid)
            
            spotify_songartist = t['artists'][0]['name']
            sporify_songartist_list.append(spotify_songartist)
    
    
    loud_list=[]
    speech_list=[]
    instrument_list = []
    
    for s in spotify_songid_list:
        unit= sp.audio_features(s)[0]
        if type(unit) is dict:
            loud=unit["loudness"]
            speech=unit["speechiness"]
            instrument = unit['instrumentalness']
        else:
            loud="NA"
            speech="NA"
            instrument="NA"  
        loud_list.append(loud)
        speech_list.append(speech)
        instrument_list.append(instrument)
    
    rowcount = cur.execute('SELECT COUNT(*) FROM now_Spotify_Data')
    index = rowcount.fetchone()[0]
  
    for time in range(index,index+20):
        cur.execute("INSERT OR IGNORE INTO now_Spotify_Data (present_id, present_title, present_popularity, present_artist,present_speechiness,present_loudness, present_instrumentalnes) VALUES (?, ?, ?, ?, ?, ?, ?)", (spotify_songid_list[time], spotify_songname_list[time], spotify_songpopu_list[time], sporify_songartist_list[time],speech_list[time],loud_list[time],instrument_list[time]))
        conn.commit() 

       

def setupOldSpotifyTable(cur,conn):
    cur.execute("CREATE TABLE IF NOT EXISTS old_Spotify_Data (old_id TEXT PRIMARY KEY,old_title TEXT, old_popularity INTEGER, old_artist TEXT,old_speechiness INTEGER,old_loudness INTEGER, old__instrumentalnes INTEGER)")
    cur.execute('SELECT old_name,old_singer FROM BillBoard')
    song_artist_list = cur.fetchall()
    
    song_list = []
    song_dict = []
    for i in range(len(song_artist_list)):
        song_list.append(song_artist_list[i][0])
    for m in song_list:
        content = sp.search(m,type="track")
        song_dict.append(content)
    
    #get track informations
    spotify_songname_list=[]
    spotify_songpopu_list=[]
    sporify_songartist_list=[]
    spotify_songid_list = []
    
    for item in song_dict:
        for t in item['tracks']['items']:
            spotify_songname = t.get("name", "")
            spotify_songname_list.append(spotify_songname)
            
            spotify_songpopu = t.get("popularity", "")
            spotify_songpopu_list.append(spotify_songpopu)
            
            spotify_songid = t.get("id", "")
            spotify_songid_list.append(spotify_songid)
            
            spotify_songartist = t['artists'][0]['name']
            sporify_songartist_list.append(spotify_songartist)
    
    #get audio features
    loud_list=[]
    speech_list=[]
    instrument_list = []
    
    for s in spotify_songid_list:
        unit= sp.audio_features(s)[0]
        if type(unit) is dict:
            loud=unit["loudness"]
            speech=unit["speechiness"]
            instrument = unit['instrumentalness']
        else:
            loud="NA"
            speech="NA"
            instrument="NA"  
        loud_list.append(loud)
        speech_list.append(speech)
        instrument_list.append(instrument)

    #insert 20 or less each time
    rowcount = cur.execute('SELECT COUNT(*) FROM old_Spotify_Data')
    index = rowcount.fetchone()[0]
  
    for time in range(index,index+20):
        cur.execute("INSERT OR IGNORE INTO old_Spotify_Data (old_id, old_title, old_popularity, old_artist,old_speechiness,old_loudness,old__instrumentalnes) VALUES (?, ?, ?, ?, ?, ?, ?)", (spotify_songid_list[time], spotify_songname_list[time], spotify_songpopu_list[time], sporify_songartist_list[time],speech_list[time],loud_list[time],instrument_list[time]))
        conn.commit() 
    





def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/mymusic.db')
    cur = conn.cursor()
    setupPresentSpotifryTable(cur,conn)
    setupOldSpotifyTable(cur,conn)
    
    conn.close()

if __name__ == "__main__":
    main()