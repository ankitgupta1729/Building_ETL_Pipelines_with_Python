# import modules
import certifi
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import urllib3
from urllib3 import request
from unicodedata import normalize
import requests

# parquet data
df_parquet=pd.read_parquet("yellow_tripdata_2024-01.parquet")
print(df_parquet.head())

url="https://data.cityofnewyork.us/resource/h9gi-nx95.json?%24limit=500"

# get data from the API
#http = urllib3.PoolManager()
#print(http.request("GET", url).status)
apt_status=requests.get(url).status_code

if apt_status == 200:
    # Sometimes we get certificate error . We should never silence this error as this may cause a securirty threat.
    # Create a Pool manager that can be used to read the API response
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    data = json.loads(http.request('GET', url).data.decode('utf-8'))
    df_api = pd.json_normalize(data)
else:
    df_api = pd.Dataframe()
print(df_api.head(10))

# Read data from relational databases

# Read sqlite query results into a pandas DataFrame
with sqlite3.connect("movies.sqlite") as conn:
    df = pd.read_sql("SELECT * from movies", conn)
print(df.head())

# Sourcing data from Webpages

# get data from url
df_html = pd.read_html('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)',match = 'by country')
# Let's see how many tables are there with tag ' by country'
print(len(df_html)) # There are 4 tables
# Let's see the first table
print(df_html[0])