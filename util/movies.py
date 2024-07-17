import requests
from sklearn.metrics.pairwise import cosine_similarity
import torch
from datetime import datetime
import numpy as np
from load import model, tokenizer
from config import Config

conf = Config()


def get_embedding(sentence):
    # Tokenize the sentence
    encoded_input = tokenizer(sentence, return_tensors="pt")

    with torch.no_grad():
        output = model(
            input_ids=encoded_input["input_ids"],
            attention_mask=encoded_input["attention_mask"],
            return_dict=True,
        )

    emb = output.last_hidden_state

    mean_emb = emb.mean(dim=1)
    return mean_emb


def find_top_movies(df, input_list, top_n=5):
    input_embedding = get_embedding(input_list)

    df["cosine_similarity"] = df["combined_embedding"].apply(
        lambda x: cosine_similarity(x.reshape(1, -1), input_embedding)[0][0]
    )

    top_25_movies = df.nlargest(25, "cosine_similarity")

    top_25_movies_sorted = top_25_movies.sort_values(by="imdb_score", ascending=False)
    final_top_movies = top_25_movies_sorted.head(top_n)

    return final_top_movies["title"].tolist()


def fetch_leatest_movies(movie_type, page=1):
    url = f"https://vidsrc.to/vapi/movie/{movie_type}/{page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("result", {}).get("items", [])
    else:
        print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        return []
