import requests
from datetime import datetime

from fastapi import APIRouter

from util import find_top_movies, fetch_leatest_movies
from load import df
from config import Config

conf = Config()
movies_router = APIRouter()


@movies_router.post(
    "/movies", tags=["Movies"], status_code=201, response_model=list[str]
)
async def run_new_movies_query(
    query_string: str,
):  # TODO: Change into different aspects from the questions, and build the query string accordingly
    res = find_top_movies(df, query_string)
    return res


@movies_router.get("/latest")
def get_latest_movies():
    all_movies = []
    page = 1

    while len(all_movies) < 50:
        movies = fetch_leatest_movies("new", page)
        if not movies:
            break 
        all_movies.extend(movies)
        page += 1
    return all_movies[:50]


# @movies_router.get("/question")
# def question_generating():
#     questions = """
#     1. Emotions: What kind of emotions do you want to feel while watching this movie/show?
#     2. Genres: What genres do you prefer for this movie/show?
#     3. Type: Do you prefer a movie or a TV show?
#     4. Length: How long do you want the movie/show to be (e.g., short, medium, long)?
#     5. Extra Field: Write whatever you feel like writing (not exceeding 30 characters).
#     """
#     return {"questions": questions}


# @movies_router.get("/latest")
# def get_latest_movies():
#     print(conf.get_tmdb_token())
#     headers = {
#         "accept": "application/json",
#         "Authorization": f"Bearer {conf.get_tmdb_token()}"
#     }
#     url = "https://api.themoviedb.org/6/movie/latest"
#     response = requests.get(url, headers=headers)
#     return response.text


# @movies_router.get("/latest")
# def get_latest_movies():
#     headers = {
#     "client": conf.get_movieglu_client(),
#     "x-api-key": conf.get_movieglu_api_key(),
#     "authorization": f"Basic {conf.get_movieglu_authorization()}",
#     "territory": conf.get_movieglu_territory(),
#     "api-version": conf.get_movieglu_api_version(),
#     "geolocation": conf.get_movieglu_geolocation(),
#     "device-datetime": datetime.utcnow().isoformat() + "Z"
# }
#     url = "https://api-gate2.movieglu.com/filmsComingSoon?n=15"
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         for film in data.get('films', []):
#             print(film.get('film_name'))
#     else:
#         print(f"Failed to retrieve data: {response.status_code} - {response.text}")
#         print(response.text)
#     return response.json()