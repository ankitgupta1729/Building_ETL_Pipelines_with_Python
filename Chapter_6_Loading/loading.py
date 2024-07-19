### Best Practices for Data Loading

# import modules
import sqlite3
import pandas as pd


# demo data
movies_data = [
    {"id": 66, "original_title": 'ankit', "budget": 100, "popularity": 12,'release_date':'12/10/2009',
       'revenue':12, 'title':'soumi', 'vote_average':9.1, 'vote_count':1200, 'overview':'good', 'tagline':'no idea',
       'uid':2121, 'director_id':432},
{"id": 69, "original_title": 'ankit', "budget": 100, "popularity": 12,'release_date':'12/10/2009',
       'revenue':12, 'title':'soumi', 'vote_average':9.1, 'vote_count':1200, 'overview':'good', 'tagline':'no idea',
       'uid':2121, 'director_id':432}
]


with sqlite3.connect("movies.sqlite") as conn:
    df = pd.read_sql("SELECT * from movies", conn)
print(df)
#print(df.columns)
#df.to_csv("movies.csv",index=False)

## Full Data Load

# def perform_full_data_load(movies_data):
#     conn = sqlite3.connect("movies.sqlite")  # Connect to the database
#     cursor = conn.cursor()
#
#     # Truncate the existing data
#     cursor.execute("DELETE FROM movies")
#
#     # Insert new data
#     for record in movies_data:
#         cursor.execute("INSERT INTO movies (id, original_title, budget, popularity,release_date,revenue, title, vote_average, vote_count, overview, tagline,uid, director_id) VALUES (?, ?, ?, ?,?, ?, ?,?,?,?,?,?,?)",
#                        (record['id'], record['original_title'], record['budget'],record['popularity'], record['release_date'],
#        record['revenue'], record['title'], record['vote_average'], record['vote_count'], record['overview'], record['tagline'],
#        record['uid'], record['director_id']))
#
#     conn.commit()
#     conn.close()
#
# perform_full_data_load(movies_data)
#
# # checking data
#
# with sqlite3.connect("movies.sqlite") as conn:
#     df = pd.read_sql("SELECT * from movies", conn)
# print(df)
# #print(df.columns)

#############################################################################

##Incremental Data Load

def perform_incremental_data_load(movies_data):
    conn = sqlite3.connect("movies.sqlite")  # Connect to the database
    cursor = conn.cursor()

    # Insert new data (if the movie doesn't already exist)
    for record in movies_data:
        cursor.execute("INSERT OR IGNORE INTO movies (id, original_title, budget, popularity,release_date,revenue, title, vote_average, vote_count, overview, tagline,uid, director_id) VALUES (?, ?, ?, ?,?, ?, ?,?,?,?,?,?,?)",
                       (record['id'], record['original_title'], record['budget'],record['popularity'], record['release_date'],
       record['revenue'], record['title'], record['vote_average'], record['vote_count'], record['overview'], record['tagline'],
       record['uid'], record['director_id']))

    conn.commit()
    conn.close()

perform_incremental_data_load(movies_data)

# checking data

with sqlite3.connect("movies.sqlite") as conn:
    df = pd.read_sql("SELECT * from movies", conn)
print(df)
#print(df.columns)
