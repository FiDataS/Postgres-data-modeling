Project: Data Modeling with Postgres - Sparkify data
=======

Introduction on the use case (Sparkify) and the project goal
-----------
Similar to real-world Spotify, Sparkify is a music streaming service that wants to analyze the data they have been collecting on user acivity on their app. Sparkify has data on their users activities, for example:
- Which pages does a user visit in their app?
- Which songs do users listen to?
- What level (free, paid) is a user on?
- etc.
In this use case the analytics team is particulary interested in understanding the song-data, so which songs users listen to. They have user data available as well as information about the songs (name, artists, duration, etc.) but no easy way to query their data. The data is stored as JSON files - one directory contains user-activity logs and the other metadata on the songs (also in JSON format). 
The goal of this project is to create a rational database (Postgres DB) with tables that organize the data for query-optimization. The tables will be organized in fact and dimension tables for a star schema. First the database is being setup (Creation of the tables with according schema, Methods for inserting data easily) and then an ETL pipeline will read in data from the directionary. 


The Database
-----------
The database is organized in a star schema - with one fact table (songplays) and 4 dimension tables (users, songs, artists, time). The following shows the columns of each table and a short explanation to its content.

### Fact Table
**songplays** - this table contains log data associated with songs - these are resulting from log-data on the app-page "NextSong" from the Sparkify app. The songplay_id is being generated through a serial datatype in postgres. The artist_id and song_id are values joined from the songs and artists table below.
*Columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

### Dimension Tables
**users** - this table shows the distinct users in the dataset, with user_id, name, gener and level they are using.
*Columns: user_id, first_name, last_name, gender, level*

**songs** - this table shows information about songs. This data does not come from the user-logs but contains only metainformation about songs.
*Columns: song_id, title, artist_id, year, duration*

**artists** - this table shows information about the artists from available songs in Sparkify. This data does not come from the user-logs but contains only metainformation about artists.
*Columns: artist_id, name, location, latitude, longitude*

**time** - this table contains timestamps from the user-logs, where a Song was played. The data is broken down into timestamp, hour, day, week, month, weekday
*Columns: start_time, hour, day, week, month, year, weekday*


Project Files
-----------

**test.ipynb** is used for checking the database if it fulfills the analyst-requirements.
**create_tables.py** creates tables newly. This file has to be run to reset the tables and create them newly. This skript has to be run each time before etl.py.
**etl.ipynb** reads and processes a single file from song_data and log_data and loads them into the table. This notebook is used to develope the algorithm for the ETL pipeline in etl.py.
**etl.py** reads and processes files from song_data and log_data and loads them into the tables. This has to be run in order to load data into the database (after create_tables.py).
**sql_queries.py** contains all the sql queries that are needed for the python scripts. Contains CREATE, INSERT and DROP statements.
**README.md** provides a description of the project and how to run it.

Steps in the etl.py
-----------
1. Song files are processed:
The song files are being opened and converted into a dataframe. Then the subsets of that dataframe are taken and inserted into song_table and artist_table. The columns in the subset are chosen according to the schema above.
     
2. Log files are processed:
The log files are being opened and converted into a dataframe. The dataframe is being filtered by events for the page "NextSong" to only get entries from users listening to songs (and not login/logout etc.). The timestamp column is then converted into timestamp type. Then the time table is created through converting the timestamp column into hour, week, month, year, weekday. Following the user table is created from a subset of that dataframe. At last the songplay table is created with a subset of data but also through a join statement on song and artist data for the song_id and artist_id information.


How to run
-----------

First the database as well as its tables are created. Therefore open a terminal and run:

```
python3 create_tables.py
```

Now that the tables are created successfully, the etl.py should be run to fill them with data. Type the following into the terminal:

```
python3 etl.py
```
The terminal should now return the progress on the files and inserts the data into the tables one by one.
