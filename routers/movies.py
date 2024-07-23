import requests
import uuid
from sqlalchemy.orm import Session
from core.schemas import schemas
from core.crud import crud
from datetime import datetime, timezone
from dependencies import get_db, validate_user_token
from core.models import tables
from core.crud.crud import create_solo_suggestions_history
from fastapi import APIRouter, Depends

from util import fetch_leatest_movies, extend_top_movies, find_top_movies
from load import df
from config import Config

conf = Config()
movies_router = APIRouter()


@movies_router.post(
    "/api/movies", tags=["Solo"], status_code=201, response_model=list[schemas.Movie]
)
async def run_new_movies_query(
    query_dict: schemas.UserAnswer,
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
):
    user_id = user.get("id")
    query_dict_list = []
    query_dict_list.append(query_dict.model_dump())
    top_movies_imdb_ids = find_top_movies(df, query_dict_list)
    res = extend_top_movies(db, top_movies_imdb_ids)
    create_solo_suggestions_history(
        db, user_id, query_dict.model_dump(), top_movies_imdb_ids
    )

    # Add a feedback row for all suggested movies, with initial feedback rate 0
    for movie in top_movies_imdb_ids:
        crud.update_movie_rating(0, movie, user_id, db)

    return res


@movies_router.get(
    "/api/movies/history",
    tags=["Solo"],
    status_code=200,
    response_model=list[schemas.SoloSuggestionsHistory],
)
async def get_solo_suggestions_history(
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(validate_user_token),
):
    user_id = user.get("id")
    return crud.get_solo_suggestions_history(db, user_id)


@movies_router.get("/api/movies/latest", tags=["Latest Movies"])
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


@movies_router.get("/api/movies/latest_with_images", tags=["Latest Movies"])
def get_latest_movies():
    headers = {
        "client": conf.get_movieglu_client(),
        "x-api-key": conf.get_movieglu_api_key(),
        "authorization": f"Basic {conf.get_movieglu_authorization()}",
        "territory": conf.get_movieglu_territory(),
        "api-version": conf.get_movieglu_api_version(),
        "geolocation": conf.get_movieglu_geolocation(),
        "device-datetime": datetime.utcnow().isoformat() + "Z",
    }
    url = "https://api-gate2.movieglu.com/filmsComingSoon?n=15"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        movie = []
        for film in data.get("films", []):
            imdb_id = film.get("imdb_id")
            film_name = film.get("film_name")
            film_image = film.get("images", {}).get("poster", {})
            if imdb_id and film_name and film_image:
                film_image = (
                    film.get("images", {})
                    .get("poster", {})
                    .get("1", {})
                    .get("medium", {})
                    .get("film_image")
                )
                movie.append(
                    {
                        "imdb_id": imdb_id,
                        "film_name": film_name,
                        "film_image": film_image,
                    }
                )
        return {"movies": movie}
    else:
        print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        print(response.text)


@movies_router.get("/api/movies/latest_imdb8", tags=["Latest Movies"])
def get_latest_movies():
    url = "https://ott-details.p.rapidapi.com/advancedsearch"

    querystring = {"start_year": "2024", "type": "movie", "page": "1"}

    headers = {
        "x-rapidapi-key": "bbcfdac50amsh60af14119911f66p18ab9fjsn77a641adfe85",
        "x-rapidapi-host": "ott-details.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        return response.json()
    else:
        return {"error": "Unable to fetch movie "}, response.status_code
