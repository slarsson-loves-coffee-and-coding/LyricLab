import streamlit as st
from functions import add_logo, add_sidebar_infos, load_dataset, create_corr_matrix, create_scatterplot


add_logo()
add_sidebar_infos()

df = load_dataset('data.csv')

numeric_list = ['All Time Rank', 'Track Score', 'Spotify Streams', 'Spotify Playlist Count',
                    'Spotify Playlist Reach', 'Spotify Popularity', 'YouTube Views', 'YouTube Likes', 'TikTok Posts',
                    'TikTok Likes', 'TikTok Views', 'YouTube Playlist Reach', 'Apple Music Playlist Count',
                    'AirPlay Spins', 'SiriusXM Spins', 'Deezer Playlist Count', 'Deezer Playlist Reach',
                    'Amazon Playlist Count', 'Pandora Streams', 'Pandora Track Stations', 'Soundcloud Streams',
                    'Shazam Counts', 'Tempo', 'Track-Popularity', 'Follower',
                    'Popularity']

df_numeric = df[numeric_list]

st.title("Korrelationen und Kausalitäten")
st.header("Hier geht's um Zusammenhänge...")

st.divider()

st.subheader("Korrelationsmatrix:")

# Korrelationsmatrix
create_corr_matrix(df_numeric.corr())

st.divider()

st.subheader("In der Tiefe...")

# Dropdown-Menüs für die Achsen
st.write("Was möchtest du vergleichen?")
x_axis = st.selectbox('Wähle die x-Achse:', options=df_numeric.columns)
y_axis = st.selectbox('Wähle die y-Achse:', options=df_numeric.columns)

if st.button("Ergebnisse plotten"):
    create_scatterplot(x_axis, y_axis, df_numeric)

st.divider()

st.subheader("Für die Statistik-Fans:")

st.write(df_numeric.describe())
