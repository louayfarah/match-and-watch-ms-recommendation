import requests
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np
from load import model, tok


def get_embeddings(text):
    enc = tok(text, return_tensors="pt")
    output = model.encoder(
        input_ids=enc["input_ids"],
        attention_mask=enc["attention_mask"],
        return_dict=True,
    )
    emb = output.last_hidden_state
    mean_emb = emb.mean(dim=1)
    return mean_emb


def find_top_movies(df, input_text, top_n=5):
    input_embedding = get_embeddings(input_text)
    input_embedding = input_embedding.detach().numpy().flatten()

    df["cosine_similarity"] = df["combined_embedding"].apply(
        lambda x: cosine_similarity([x.flatten()], [input_embedding])[0][0]
    )

    top_movies = df.sort_values(by="cosine_similarity", ascending=False).head(top_n)
    return top_movies["title"].tolist()


def fetch_leatest_movies(movie_type, page=1):
        url = f"https://vidsrc.to/vapi/movie/{movie_type}/{page}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('result', {}).get('items', [])
        else:
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")
            return []