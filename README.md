# 🎬 CineMatch — AI-Powered Movie Recommender

> *Tell us one film you love. We'll find five more you'll adore.*

CineMatch is a full-stack movie recommendation system — a **FastAPI** backend serving a content-based ML model, paired with a **Streamlit** frontend styled with a dark, cinematic UI. Pick any film, hit **Discover**, and receive five tailored recommendations with posters fetched live from TMDB.

---

## 🗂️ Project Structure


```
CineMatch
├─ backend
│  ├─ app
│  │  ├─ main.py
│  │  └─ model
│  │     └─ model.pkl
|  |     |_ model_dict.pkl 
│  └─ requirements.txt
└─ frontend
   ├─ app.py
   ├─ Dockerfile
   └─ requirements.txt

```

---

## ⚙️ How It Works

```
User selects a movie
        │
        ▼
Streamlit (app.py)  ──POST /recommend──►  FastAPI (main.py)
                                                │
                                        Looks up movie index
                                        in movie_dict DataFrame
                                                │
                                        Computes top-5 similar
                                        movies via cosine similarity
                                        matrix (movie.pkl)
                                                │
                                        Fetches poster for each
                                        from TMDB API
                                                │
                    ◄── JSON response ──  Returns titles + poster URLs
        │
        ▼
Streamlit renders 5 animated movie cards
```

The recommendation model is **content-based filtering** — similarity scores are pre-computed and stored in a pickled matrix, so inference is near-instant.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A free [TMDB API key](https://developer.themoviedb.org/docs/getting-started)

---

### 1 — Backend (FastAPI)

```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install fastapi uvicorn pandas requests gdown python-dotenv pydantic

# Create your .env file
echo "TMDB_API_KEY=your_tmdb_api_key_here" > .env

# Start the server
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`.

> **Note:** On first run, `main.py` automatically downloads the two model files (`movie.pkl` and `movie_dict.pkl`) from Google Drive using `gdown`. This may take a moment.

---

### 2 — Frontend (Streamlit)

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
pip install streamlit requests

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

> If running the backend locally, update `API_URL` in `app.py`:
> ```python
> API_URL = "http://localhost:8000"
> ```

---

## 🔌 API Reference

Base URL: `https://movie-recommender-pn4m.onrender.com`

### `GET /health`

Health check — used by Render to keep the service alive.

```json
{ "status": "ok" }
```

---

### `GET /movies`

Returns all available movie titles.

```json
{
  "movies": ["The Dark Knight", "Inception", "Interstellar", "..."]
}
```

---

### `POST /recommend`

Returns 5 recommended movies with poster URLs.

**Request body**
```json
{ "movie": "Inception" }
```

**Response `200`**
```json
{
  "recommended_movies": [
    { "title": "The Prestige",   "poster_url": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "Memento",        "poster_url": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "Shutter Island", "poster_url": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "Interstellar",   "poster_url": "https://image.tmdb.org/t/p/w500/..." },
    { "title": "The Matrix",     "poster_url": "https://image.tmdb.org/t/p/w500/..." }
  ]
}
```

**Response `404`**
```json
{ "error": "Movie not found" }
```

---

## 🌍 Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

| Variable | Required | Description |
|---|---|---|
| `TMDB_API_KEY` | ✅ Yes | API key from [themoviedb.org](https://developer.themoviedb.org) |

---

## ☁️ Deployment

### Backend — Render

1. Push the backend to a GitHub repository
2. Create a new **Web Service** on [Render](https://render.com)
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add `TMDB_API_KEY` as an environment variable in the Render dashboard
6. Deploy — model files are downloaded automatically on first boot via `gdown`

### Frontend — Streamlit Community Cloud

1. Push the frontend to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set `app.py` as the entry point
4. Deploy — no environment variables needed for the frontend

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + custom HTML/CSS |
| Backend | FastAPI + Uvicorn |
| ML Model | Content-based filtering (cosine similarity) |
| Data | Pandas DataFrame (pickled) |
| Poster Images | [TMDB API](https://developer.themoviedb.org) |
| Model Storage | Google Drive via `gdown` |
| Hosting | Render (API) · Streamlit Cloud (UI) |

---

## 🐛 Troubleshooting

**The movie list takes a long time to load**
The backend runs on Render's free tier and spins down after inactivity. The first request after a sleep period may take 30–60 seconds. Subsequent requests are fast.

**`TMDB_API_KEY` errors on startup**
Ensure your `.env` file exists in the same directory as `main.py` and contains a valid key. You can verify it loaded correctly with a quick `print(os.getenv("TMDB_API_KEY"))` in a Python shell.

**`gdown` fails to download model files**
Google Drive imposes a download quota. If it's exceeded, try again after a few hours — or host the `.pkl` files yourself and update the `id=` values in the `gdown.download()` calls inside `main.py`.

**Posters show a placeholder image**
TMDB returned a null `poster_path` for that film, or the movie ID in the dataset doesn't match TMDB's current catalogue. The frontend handles this gracefully with a fallback image.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Made with ☕ and a love of cinema</p>
