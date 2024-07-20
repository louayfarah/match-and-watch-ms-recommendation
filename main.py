from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import movies_router, session_router, feedback_router

from routers import movies_router
from core.databases.postgres.postgres import engine
from core.models import tables

load_dotenv()  # Load environmental variables

# Create the backend application
app = FastAPI()

tables.Base.metadata.create_all(bind=engine)

# Allow all origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(movies_router)
app.include_router(session_router)
app.include_router(feedback_router)


# Define the root source
@app.get("/", tags=["Root"], status_code=200)
async def root():
    return {"message": "The recommendation microservice is up!"}
