import streamlit as st
import streamlit as st
import pandas as pd
from functions import add_logo, add_sidebar_infos, prepare_lyrics, load_and_prepare_lyrics, vectorize_songs

# Für Lyrics:
from lyricsgenius import Genius

# Genius API:
token = st.secrets.genius_token
genius = Genius(token)
genius.remove_section_headers = False
genius.verbose = True


#######################################################################################################################
#######################################################################################################################




#######################################################################################################################
#######################################################################################################################


add_logo()
add_sidebar_infos()

df = pd.read_csv('spotify-data_lyrics.csv')

# Main content
# Überschrift Homepage
st.markdown("""
<style>
.big-font {
  font-size: 24px;
  text-align: center;
}
</style>

<p class="big-font">Willkommen bei</p>
""", unsafe_allow_html=True)

# Titelbild
st.markdown("""
<div style="text-align: center;">
  <img src="https://i.imgur.com/F3tDM34.png" alt="Mein Logo">
</div>
""", unsafe_allow_html=True)

# Schrift unterm Bild
st.markdown("""
<style>
.big-font {
  font-size: 24px;
  text-align: center;
}
</style>

<p class="big-font">...<span style="font-style: italic;">der</span> App zum Analysieren von Songs und Songtexten!</p>
""", unsafe_allow_html=True)

#######################################################################################################################
#######################################################################################################################

st.divider()
st.write("Du hast einen Song geschrieben und bist unsicher, ob er wirklich ein Hit wird? Du willst wissen, welche Top-Words einen Song wirklich erfolgreich machen?")
st.write("Gib deinen Song hier ein und lass dir zeigen, welchen Top-Hits er am meisten ähnelt:")

new_song = st.text_area("Eingabe:")
new_song_result = prepare_lyrics(new_song)

if st.button("Deinen Songtext vergleichen"):
    vectorize_songs(df, new_song_result)

#######################################################################################################################
#######################################################################################################################

st.divider()

st.write("Du hast gar keinen Song geschrieben, willst die App aber trotzdem testen?")
st.write("Kein Problem! Suche hier nach einem Song deiner Wahl und vergleiche die Lyrics untereinander:")

test_song_track = st.text_input("Titel:")
test_song_artist = st.text_input("Interpret:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Songtext laden"):
        try:
            song = genius.search_song(test_song_track, test_song_artist)
            song.lyrics
        except Exception as e:
            st.write(f"Der gewünschte Song konnte leider nicht gefunden werden.\n Probier es gern noch einmal!")

with col2:
    pass

with col3:
    if st.button("Diesen Songtext vergleichen"):
        try:
            test_song_result = load_and_prepare_lyrics(test_song_track, test_song_artist)
            vectorize_songs(df, test_song_result)
        except Exception as e:
            st.write(f"Der gewünschte Song konnte leider nicht gefunden werden.\n Probier es gern noch einmal!")
