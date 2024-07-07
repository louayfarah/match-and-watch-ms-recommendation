from fastapi import APIRouter
from util import find_top_movies
from load import df


movies_router = APIRouter()


@movies_router.post(
    "/movies", tags=["Movies"], status_code=201, response_model=list[str]
)
async def run_new_movies_query(
    query_string: str,
):  # TODO: Change into different aspects from the questions, and build the query string accordingly
    res = find_top_movies(df, query_string)
    return res
