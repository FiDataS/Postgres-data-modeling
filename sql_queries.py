# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# SERIAL datatype is an autoincrement data type, postgre will manage itself; It is automatically/per definition NOT NULL, It will generate an integer value and assign it to the column whenever data is inserted into the table (hence column will always be NOT NULL) 

songplay_table_create = (""" 
    CREATE TABLE IF NOT EXISTS songplays
    (songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP REFERENCES time(start_time) NOT NULL, 
    user_id INT REFERENCES users(user_id) NOT NULL,
    level VARCHAR, 
    song_id VARCHAR REFERENCES songs(song_id), 
    artist_id VARCHAR REFERENCES artists(artist_id), 
    session_id INT, 
    location VARCHAR, 
    user_agent VARCHAR); 
    """)

# PRIMARY KEY: This column is a primary key, which implies that other tables may rely on this column as a unique identifier for rows. Both UNIQUE and NOT NULL are implied by PRIMARY KEY

# REFERENCES: The REFERENCES column constraint specifies that a column of a table must only contain values which match against values in a referenced column of a referenced table.
# A value added to this column is matched against the values of the referenced table and referenced column using the given match type. In addition, when the referenced column data is changed, actions are run upon this column's matching data. (https://www.postgresql.org/docs/7.1/sql-createtable.html)
# Consider the following problem: You want to make sure that no one can insert rows in the weather table that do not have a matching entry in the cities table. This is called maintaining the referential integrity of your data. In simplistic database systems this would be implemented (if at all) by first looking at the cities table to check if a matching record exists, and then inserting or rejecting the new weather records. This approach has a number of problems and is very inconvenient, so PostgreSQL can do this for you. Source: https://www.postgresql.org/docs/current/tutorial-fk.html 

user_table_create = (""" 
    CREATE TABLE IF NOT EXISTS users
    (user_id INT PRIMARY KEY,
    first_name VARCHAR, 
    last_name VARCHAR, 
    gender VARCHAR, 
    level VARCHAR); 
    """)

#Changed with Not NULL
song_table_create = (""" 
    CREATE TABLE IF NOT EXISTS songs
    (song_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL, 
    artist_id VARCHAR, 
    year INT, 
    duration FLOAT NOT NULL); 
    """)

#changed with Not NULL
artist_table_create = (""" 
    CREATE TABLE IF NOT EXISTS artists
    (artist_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    latitude FLOAT,
    longitude FLOAT); 
    """)

time_table_create = (""" 
    CREATE TABLE IF NOT EXISTS time
    (start_time TIMESTAMP PRIMARY KEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT); 
    """)

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays
    (start_time, 
    user_id, 
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location, 
    user_agent) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

# if a user changes from level = free to level = paid, we want to update that field
# therefore the ON CONFLICT clause is changed to the following
# source: https://learn.udacity.com/nanodegrees/nd027/parts/cd0029/lessons/ls1960/concepts/9e0a958d-7a5e-4896-ab95-98a4c4bccb67
# source 2: https://www.postgresql.org/docs/9.5/sql-insert.html ("Assumes a unique index has been defined that constrains values appearing in the did column")

user_table_insert = ("""
    INSERT INTO users
    (user_id,
    first_name, 
    last_name, 
    gender, 
    level) 
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id,
    title, 
    artist_id, 
    year, 
    duration)  
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists
    (artist_id,
    name,
    location,
    latitude,
    longitude)   
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time
    (start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday)  
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

# find song ID and artist ID based on the title, artist name and duration of song from songs and artists table
song_select = ("""
    SELECT s.song_id, a.artist_id
    FROM songs AS s JOIN artists AS a ON s.artist_id = a.artist_id
    WHERE s.title = %s AND a.name = %s AND s.duration = %s;
""")


# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]