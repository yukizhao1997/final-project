from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import sqlite3


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setupBillboardTable(cur, conn):
    now_url = "https://www.billboard.com/charts/hot-100"
    r = requests.get(now_url)
    now_soup = BeautifulSoup(r.text, "lxml")
    
    old_url="https://www.billboard.com/charts/hot-100/1970-04-11"
    old_r = requests.get(old_url)
    old_soup = BeautifulSoup(old_r.text, "lxml")


    now_song_list =[]
    now_artist_list =[]
    now_songs = now_soup.find_all('span', class_='chart-element__information__song text--truncate color--primary')
    now_artists = now_soup.find_all('span', class_='chart-element__information__artist text--truncate color--secondary')
    for now_song in now_songs:
        now_song_list.append(now_song.text)
    for now_artist in now_artists:
        now_artist_list.append(now_artist.text)
    

    old_song_list =[]
    old_artist_list =[]
    old_songs = old_soup.find_all('span', class_='chart-element__information__song text--truncate color--primary')
    old_artists = old_soup.find_all('span', class_='chart-element__information__artist text--truncate color--secondary')
    for old_song in old_songs:
        old_song_list.append(old_song.text)
    for old_artist in old_artists:
        old_artist_list.append(old_artist.text)
    

    cur.execute("DROP TABLE IF EXISTS BillBoard")
    cur.execute("CREATE TABLE BillBoard (now_name TEXT, now_singer TEXT, old_name TEXT, old_singer TEXT)")
    for i in range(100):
        cur.execute("INSERT INTO BillBoard (now_name,now_singer,old_name,old_singer) VALUES (?,?,?,?)",(now_song_list[i],now_artist_list[i], old_song_list[i],old_artist_list[i]))
    conn.commit()


def main():
    cur,conn = setUpDatabase('mymusic.db')

    setupBillboardTable(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()
