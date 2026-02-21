import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.title('Movie Recommender')

@st.cache_data
def fetch_movies():
    res = requests.get(f"{API_URL}/movies")
    return res.json()["movies"]

def fetch_recommended_movies(option):
    try:
        res = requests.post(f"{API_URL}/recommend",json={"movie":option})
        
        if res.status_code == 200:
            recommendations = res.json()["recommended movies"]
            return recommendations
    except Exception as e:
        st.error(f"Could not fetch recommendations: {e}")
        return []


movie_list = fetch_movies()

option = st.selectbox(
    "Select a movie?",
    (movie_list),
)

st.write("You selected:", option)



if (st.button("Recommend", type="primary")):
    recs = fetch_recommended_movies(option)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    if recs:
        with col1:
            st.text(recs[0]["title"])
            st.image(recs[0]["poster_url"])

        with col2:
            st.text(recs[1]["title"])
            st.image(recs[1]["poster_url"])

        with col3:
            st.text(recs[2]["title"])
            st.image(recs[2]["poster_url"])
            
        with col4:
            st.text(recs[3]["title"])
            st.image(recs[3]["poster_url"])
            
        with col5:
            st.text(recs[4]["title"])
            st.image(recs[4]["poster_url"])

