import pandas as pd
import sqlite3

conn = sqlite3.connect('movies.db')# connect to database
cur = conn.cursor() # forming a curser to execute sqlite commands in python
# creating a table
cur.execute('''CREATE TABLE IF NOT EXISTS favorite_movies
                (year_x INTEGER,
                name  TEXT,
                star TEXT,
                gender TEXT,
                director text)''')

df=pd.read_csv("movies.csv")#reading first fime
df1=pd.read_csv("movie2.csv")#reading second file
df=pd.merge(df,df1,how="outer" ,on="name")# merging both the files on column name
df=df.loc[:,["name","score","votes","director","star","gender","language",'year_x']]#selecting the required columns for cleaning data
df=df.dropna()
df=df[df["score"]>8].dropna()# selecting movies having rating greater then 8
df=df[df['language']=="['English']"].dropna()# my favorite_movies are mostly english
df=df[df["votes"]>100000].dropna()# selecting maximum votes

df=df.loc[:,["name","star","gender","director",'year_x']]#selecting the required columns
df=df.drop_duplicates(subset="name", keep='first', inplace=False)#delete all the duplicates
#setting index as year
df = df.set_index("year_x")
df=df.sort_index()

df.to_sql('favorite_movies', conn, if_exists='replace', index=True)#transferring data to database
# some more inserting into table
cur.execute('''INSERT INTO favorite_movies (year_x , name , star , gender , director ) VALUES (?, ?, ?, ?, ?)''',
           (2009,"3 Idiots","Amir Khan","male","Rajkumar Hirani"))
conn.commit()

# to delete from TABLE
# cur.execute('''DELETE FROM favorite_movies WHERE name="3 Idiots" ''')

# to print all the movie name
cur.execute('''SELECT * FROM favorite_movies''')
all_top_movies =cur.fetchall()

for mov in all_top_movies:
    mov=str(mov)
    mov=mov.split(",")
    print(mov[1])
