import requests
from datetime import datetime, timezone

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
    total_movies = 50
    page = 1

    while len(all_movies) < total_movies:
        movies = fetch_leatest_movies("new", page)
        if not movies:
            break 
        all_movies.extend(movies)
        page += 1
    return all_movies


@movies_router.get("/latest_with_images")
def get_latest_movies():
    headers = {
    "client": conf.get_movieglu_client(),
    "x-api-key": conf.get_movieglu_api_key(),
    "authorization": f"Basic {conf.get_movieglu_authorization()}",
    "territory": conf.get_movieglu_territory(),
    "api-version": conf.get_movieglu_api_version(),
    "geolocation": conf.get_movieglu_geolocation(),
    "device-datetime": datetime.utcnow().isoformat() + "Z"
 }
    url = "https://api-gate2.movieglu.com/filmsComingSoon?n=15"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        movie = []
        for film in data.get('films', []):
            imdb_id = film.get("imdb_id")
            film_name = film.get("film_name")
            film_image = film.get("images", {}).get("poster", {})
            if imdb_id and film_name and film_image:
                film_image = film.get("images", {}).get("poster", {}).get("1", {}).get("medium", {}).get("film_image")
                movie.append({
                    "imdb_id": imdb_id,
                    "film_name": film_name,
                    "film_image": film_image
                })
        return {"movies": movie}
    else:
        print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        print(response.text)




@movies_router.get("/latest_imdb8")
def get_latest_movies():
    url = "https://ott-details.p.rapidapi.com/advancedsearch"

    querystring = {"start_year":"2024","type":"movie","page":"1"}

    headers = {
        "x-rapidapi-key": "bbcfdac50amsh60af14119911f66p18ab9fjsn77a641adfe85",
        "x-rapidapi-host": "ott-details.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code==200:
        data=response.json()
        return response.json()
    else:
        return {"error": "Unable to fetch movie "}, response.status_code


