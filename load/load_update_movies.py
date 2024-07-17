import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import engine

from load import df

# Generate a uuid for each row in df
df["id"] = [uuid.uuid4() for _ in range(len(df))]

# Select the columns you want to insert into the database
columns = [
    "id",
    "imdb_id",
    "title",
    "type",
    "description",
    "release_year",
    "age_certification",
    "runtime",
    "genres",
    "imdb_score",
    "emotions",
    "length",
    "platform",
]
df_to_insert = df[columns]


# Insert the dataframe into the 'movies' table in your database
df_to_insert.to_sql("movies", engine, if_exists="append", index=False)
