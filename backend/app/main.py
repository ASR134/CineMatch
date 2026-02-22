from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
import pickle
import os
import requests
import gdown
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# paths

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_PATH = os.path.join(BASE_DIR, "model", "movie.pkl")
DICT_PATH = os.path.join(BASE_DIR, "model", "movie_dict.pkl")

# download models if not present

def download_models():
    os.makedirs(os.path.join(BASE_DIR, "model"), exist_ok=True)
    if not os.path.exists(SIM_PATH):
        gdown.download(id="1LNtGsom8cegcHntUn-5cCQZbEkcM4NGa", output=SIM_PATH, quiet=False)
    if not os.path.exists(DICT_PATH):
        gdown.download(id="1Ymo94q5WiZzmOf-sWDii-j8wVoH89YZE", output=DICT_PATH, quiet=False)

download_models()

# load model
with open(SIM_PATH, "rb") as f:
    similarity = pickle.load(f)
with open(DICT_PATH, "rb") as f:
    movie_dict = pickle.load(f)



df = pd.DataFrame(movie_dict)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )


# pydantic model

class movie_input(BaseModel):
    
    movie : Annotated[str, Field(..., description="Name of the Movie")]



def movie_poster_url(movie_id):
    search_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}" # movie details
    res = requests.get(search_url,timeout=60)
    res.raise_for_status()
    
    data = res.json()
    poster_url = data["poster_path"]
    
    if poster_url: 
        return f"https://image.tmdb.org/t/p/w500{poster_url}"
    return None
    
    
# api endpoints


# Render pings this nicely
@app.get("/health")
def health():
    return {"status": "ok"}



@app.get("/movies")
def get_movies():
    return {"movies":df["title"].to_list()}



@app.post("/recommend")
def movie_recommendations(user_input : movie_input):
    
    movie_name = user_input.movie  # input movie
    
    if movie_name not in df["title"].values:
        return JSONResponse(status_code=404, content={"error": "Movie not found"})
    
    
    movie_index  = df[ df["title"]==movie_name ].index[0]
    
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6] # list of tuples
    
    L_movies = []
    
    for i in movies_list: # (index, angle)
        index = i[0]
        url = movie_poster_url(df.iloc[index,0])
        L_movies.append({
            "title" : df.iloc[index,1],
            "poster_url" : url
            })
        
        
    return JSONResponse(status_code=200,content={"recommended_movies" : L_movies})
        
