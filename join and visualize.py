
import unittest
import sqlite3
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd 



def setup_table(cur, conn):
    
    cur.execute('CREATE TABLE IF NOT EXISTS Join_table_old AS SELECT old_title,old_artist,MAX(old_popularity) AS max_popu, old_loudness,old_speechiness,old__instrumentalnes FROM(SELECT old_Spotify_Data.old_title,old_artist,old_popularity, old_loudness,old_speechiness,old__instrumentalnes, BillBoard.old_name,old_singer FROM BillBoard LEFT JOIN old_Spotify_Data ON BillBoard.old_singer=old_Spotify_Data.old_artist AND BillBoard.old_name = old_Spotify_Data.old_title) GROUP BY old_title')
    cur.execute('CREATE TABLE IF NOT EXISTS Join_table_now AS SELECT present_title,present_artist,MAX(present_popularity) AS max_popu, present_loudness,present_speechiness,present_instrumentalnes FROM(SELECT now_Spotify_Data.present_title,present_artist,present_popularity, present_loudness,present_speechiness,present_instrumentalnes, BillBoard.now_name,now_singer FROM BillBoard LEFT JOIN now_Spotify_Data ON BillBoard.now_singer=now_Spotify_Data.present_artist AND BillBoard.now_name = now_Spotify_Data.present_title) GROUP BY present_title')
    
    cur.execute('ALTER TABLE Join_table_old ADD table_type')
    cur.execute('SELECT * FROM Join_table_old')
    cur.execute(''' UPDATE Join_table_old
                    SET table_type= 'old'  
                ''')
                
    cur.execute('ALTER TABLE Join_table_now ADD table_type')
    cur.execute('SELECT * FROM Join_table_now')
    cur.execute(''' UPDATE Join_table_now
                SET table_type= 'now'  
                ''')
                
    cur.execute('CREATE TABLE IF NOT EXISTS final_table AS SELECT * FROM Join_table_old UNION ALL SELECT * FROM Join_table_now')


def calculation(cur,conn):
    
    cur.execute('SELECT AVG(old_loudness) , AVG(old__instrumentalnes), AVG(old_speechiness)FROM final_table GROUP BY table_type')
    ave_data = cur.fetchall()
    
    with open("calculation.txt", 'w') as f:        
        f.write("average loudness of 2020 top 100 songs are "+str(ave_data[0][0])+
                "\naverage loudness of 1970 top 100 songs are "+str(ave_data[1][0])+
                "\naverage instrumentalness of 2020 top 100 songs are "+str(ave_data[0][1])+
                "\naverage instrumentalness of 1970 top 100 songs are "+str(ave_data[1][1])+
                "\naverage speechiness of 2020 top 100 songs are "+str(ave_data[0][2])+
                "\naverage speechiness of 1970 top 100 songs are "+str(ave_data[1][2]))
    f.close()



def visualize(cur, conn):
    cur.execute('SELECT * FROM final_table')
    data_list = cur.fetchall()
    
    loud_list=[]
    speech_list=[]
    instrumental_list=[]
    type_list=[]
    
    for i in data_list:
        loud_list.append(i[3])
        speech_list.append(i[4])
        instrumental_list.append(i[5])
        type_list.append(i[6])
        
    df = pd.DataFrame({'loudness': loud_list,
                    'speechiness': speech_list,
                    'instrumentalnes': instrumental_list,
                    'type': type_list})
    
    df=df.dropna()
    df["type"] = df["type"].astype('category')
    
    # scatter plot
    fig1= px.scatter(df, x="speechiness", y="instrumentalnes", color="type")
    fig1.update_yaxes(tickvals=[0,0.02,0.04,0.06,0.08,0.1])
    fig1.show()
    
    # box plot
    fig2 = px.box(df, x="type", y="speechiness")
    fig2.show()
    
    fig3 = px.box(df, x="type", y="instrumentalnes")
    fig3.show()
    
    fig4 = px.box(df, x="type", y="loudness")
    fig4.show()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/mymusic.db')
    cur = conn.cursor()
    setup_table(cur, conn)
    calculation(cur,conn)
    visualize(cur, conn)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()





