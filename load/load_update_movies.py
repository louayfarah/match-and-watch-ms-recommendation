import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import engine

from load import df

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

# Group by 'title' and aggregate the other columns
df_to_insert = (
    df_to_insert.groupby("title")
    .agg(
        {
            "id": "first",
            "imdb_id": "first",
            "type": "first",
            "description": "first",
            "release_year": "first",
            "age_certification": "first",
            "runtime": "first",
            "genres": "first",
            "imdb_score": "first",
            "emotions": "first",
            "length": "first",
            "platform": " ".join,  # Concatenate platform values
        }
    )
    .reset_index()
)

# Generate a uuid for each row in df
df_to_insert["id"] = [uuid.uuid4() for _ in range(len(df_to_insert))]

# Insert the dataframe into the 'movies' table in your database
df_to_insert.to_sql("movies", engine, if_exists="append", index=False)
