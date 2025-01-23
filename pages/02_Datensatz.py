import streamlit as st
import pandas as pd


from functions import add_logo, add_sidebar_infos, load_dataset


add_logo()
add_sidebar_infos()


st.title("Most Streamed Songs auf Spotify 2024")

st.header("Der Datensatz")

df = load_dataset('data.csv')
df_show = df.drop("Track_Artist", axis = 1)
st.write(df_show)

st.subheader("Der Ursprungsdatensatz:")
st.markdown("[Most Streamed Spotify Songs 2024](https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024) von Nidula Elgiriyewithana")

st.divider()

st.subheader("Anpassungen:")
st.markdown("* Spalte :red-background[TIDAL Popularity] entfernen (enthält keine Werte)")
st.markdown("* Spalte :green-background[Release Year] und :green-background[Release Country] hinzufügen")
st.markdown("* :red[Kommas] als Tausender-Trennzeichen entfernt")
st.markdown("* Punkt durch Komma ersetzt")
st.markdown("* Explicit 0 durch 'nein' und 1 durch 'ja' ersetzt")
st.markdown("* :red[Duplikate] entfernt")

st.divider()

st.subheader("Zusatzinformationen:")
st.markdown("**Audio-Features** über songbpm.com:")
st.markdown("* mit _requests_ und _BeautifulSoup_ Spalten :green-background[Stimmung],:green-background[Tempo],:green-background[Key],:green-background[Mode],:green-background[Energy],:green-background[Daceability] und :green-background[Beats per Bar] hinzugefügt")
st.markdown("* unnötige Strings aus den Daten entfernt")
st.markdown("**Weitere Infos** über Spotify:")
st.markdown("* mit _spotipy_ (basierend auf Spotify API) Spalten :green-background[Track-URI],:green-background[Album],:green-background[Track-Popularity],:green-background[Track-Bild], :green-background[Artist-URI],:green-background[Follower],:green-background[Genre],:green-background[Popularity] und :green-background[Artist-Bild] hinzugefügt")

st.divider()

st.subheader("Datensätze verbinden:")
st.markdown("* über Track-Artist-Kombination alle drei Datensätze zu einem verbinden")
st.markdown("* erneut Duplikate entfernt")
st.markdown("")
st.markdown("**Neuer Datensatz:** _data.csv_")


st.divider()

st.subheader("Der Lyrics-Datensatz")
df_lyrics = pd.read_csv('spotify-data_lyrics.csv', encoding='unicode_escape')
st.write(df_lyrics)

st.subheader("Der Ursprungsdatensatz:")
st.markdown("data.csv (vor Audiofeatures und Zusatzinformationen)")

st.subheader("Anpassungen:")
st.markdown("Bereinigung über Google Sheets:")
st.markdown("* Länge des Datensatzes vorerst auf alle Tracks mit mehr als 1 Mrd. Streams reduziert :arrow_right: ca. 500 Zeilen für Scraping")
st.markdown("* Codierung der Satz- und Sonderzeichen in der Spalte 'Track' (teilweise manuell) angepasst und dabei alle :red[nicht-englischen Titel] entfernt")

st.markdown("**Lyrics** über Genius:")
st.markdown("* mit _lyricsgenius_(basierend auf Genius API) Spalte :green-background[Lyrics] hinzugefügt")

st.subheader("Weitere Anpassungen:")
st.markdown("* :red[Stopwords (s. Textanalyse)], :red[Sonderzeichen] und :red[mehrfach vorkommende Wörter] entfernt")