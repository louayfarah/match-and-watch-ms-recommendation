import pandas as pd

# List of embeddings
files = [
    "data/Amazon_embedding.h5",
    "data/Disney_embedding.h5",
    "data/HBO_embedding.h5",
    "data/Netflix_embedding.h5",
    "data/Paramount_embedding.h5",
]

# Load all embeddings
dfs = []
for file in files:
    df = pd.read_hdf(file, key="df")
    platform = file.split("/")[1].split("_")[0]  # Extract platform name from file name
    df["platform"] = platform  # Add new column
    dfs.append(df)

# Concatenate all embeddings
df = pd.concat(dfs)
