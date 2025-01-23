# Verwendete Module und Bibliotheken
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from collections import Counter
from wordcloud import WordCloud
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re

# Machine Learning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Für Lyrics:
from lyricsgenius import Genius

# Genius API:
token = st.secrets.genius_token
genius = Genius(token)
genius.remove_section_headers = False
genius.verbose = True


############################################################################################################
######                                    ALLGEMEINE FUNKTIONEN                                       ######
############################################################################################################

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://i.ibb.co/GndN02D/logo2.png');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-size: contain;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def add_sidebar_infos():
    st.sidebar.header("Willkommen auf LyricLab!")
    st.sidebar.markdown(
        "Hier kannst du deine selbstgeschriebenen Songtexte analysieren und mit den Top-Hits vergleichen!")
    # st.sidebar.markdown("**Wichtige Hinweise:**")
    # st.sidebar.markdown("* (folgt in Kürze)")

def load_dataset(dataset):
    df = pd.read_csv(dataset, encoding='unicode_escape')

    categorical_cols = ['Track', 'Artist', 'ISRC', 'Release Year', 'Stimmung', 'Tempo', 'Key', 'Mode', 'Energy',
                        'Danceability',
                        'Track-URI', 'Album', 'Track-Bild', 'Artist-URI', 'Genre', 'Artist-Bild']

    numeric_cols = ['All Time Rank', 'Track Score', 'Spotify Streams', 'Spotify Playlist Count',
                    'Spotify Playlist Reach', 'Spotify Popularity', 'YouTube Views', 'YouTube Likes', 'TikTok Posts',
                    'TikTok Likes', 'TikTok Views', 'YouTube Playlist Reach', 'Apple Music Playlist Count',
                    'AirPlay Spins', 'SiriusXM Spins', 'Deezer Playlist Count', 'Deezer Playlist Reach',
                    'Amazon Playlist Count', 'Pandora Streams', 'Pandora Track Stations', 'Soundcloud Streams',
                    'Shazam Counts', 'Tempo', 'Track-Popularity', 'Follower',
                    'Popularity']

    df[numeric_cols] = df[numeric_cols].astype(float)
    df[categorical_cols] = df[categorical_cols].astype(str)
    df[categorical_cols] = df[categorical_cols].replace("nan", np.nan)
    df['Key'] = df['Key'].str.replace("â¯", "♯")
    df['Key'] = df['Key'].str.replace("â­ÂÂ", "♭")
    df['Explicit Track'] = df['Explicit Track'].replace(0, "nein")
    df['Explicit Track'] = df['Explicit Track'].replace(1, "ja")
    df['Release Country'] = [x[:2] for x in df['ISRC']]
    df = df.drop_duplicates()

    return df

############################################################################################################
######                                             HOME                                               ######
############################################################################################################

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = np.array(text.split())
    mask = ~np.isin(words, list(stop_words))
    return ' '.join(words[mask])

def prepare_lyrics(song):
    new_song_list = []
    song = re.sub(r"\s+", " ", song).lower()
    song = re.sub(r"[,.!?;()]", "", song)
    words = song.split()
    single_words = set(words)
    song = ' '.join(single_words)
    song = remove_stopwords(song)
    new_song_list.append(song)

    return new_song_list

def load_and_prepare_lyrics(track, artist):
    """
    Diese Funktion nimmt die Parameter track und artist entgegen und lädt die passenden Lyrics über die Genius API.
    Dann werden Zeilenumbrüche, diverse Sonderzeichen sowie die offiziellen englischen Stopwords und alle doppelten Worte entfernt.
    """
    song_list = []
    song = genius.search_song(track, artist)
    song_lyrics = song.lyrics
    song_lyrics = re.sub(r"\s+", " ", song_lyrics).lower()
    song_lyrics = re.sub(r"[,.!?;()]", "", song_lyrics)
    words = song_lyrics.split()
    single_words = set(words)
    song_lyrics = ' '.join(single_words)

    song_lyrics = remove_stopwords(song_lyrics)
    song_list.append(song_lyrics)

    return song_list

def vectorize_songs(df, new_song):
    # Vorhandene Texte vektorisieren und Array erstellen
    vectorizer = TfidfVectorizer()
    wordsCountArray = vectorizer.fit_transform(df['Lyrics'].values)
    X = wordsCountArray

    # Neuen Text vektorisieren
    new_text_vector = vectorizer.transform(new_song)

    # Cosine Similarity berechnen
    similarity = cosine_similarity(new_text_vector, X)

    # Ähnlichste Texte finden
    most_similar_indices = list(similarity.argsort()[0][-5:])  # Finde die 5 ähnlichsten Texte

    for index in most_similar_indices:
        similarity_percentage = similarity[0, index] * 100
        similar_track = df.loc[index, 'Track']
        similar_track_artist = df.loc[index, 'Artist']
        st.write(f"Dein Songtext ähnelt '{similar_track}' von {similar_track_artist} zu {similarity_percentage:.2f}%.")

############################################################################################################
######                                         TEXTANALYSE                                            ######
############################################################################################################

# Funktion zur Erstellung der WordCloud
def create_wordcloud():
    df = pd.read_csv('spotify-data_lyrics.csv')
    # Textdaten extrahieren:
    lyrics = " ".join(df['Lyrics'])
    wordcloud = WordCloud(width=1600, height=1600, background_color="black", colormap="Greens", mode="RGBA").generate(lyrics)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# Funktion zur Erstellung der Wortliste
def print_wordlist(num_words):
    df = pd.read_csv('spotify-data_lyrics.csv')
    text_column = df['Lyrics']
    # Split text
    all_words = []
    for text in text_column:
        words = text.split()
        all_words.extend(words)

    word_counts = Counter(all_words)

    # Most common words
    for word, count in word_counts.most_common(num_words):

        st.write(f"Das Wort '{word}' ist in {count} Songs enthalten. Damit kommt es in {count/len(text_column)*100:.0f}% der Songs vor.")

# Funktion zum Suchen nach bestimmten einzelnen Wörtern
def search_word(word):
    word_lower = word.lower()
    df = pd.read_csv('spotify-data_lyrics.csv')
    text_column = df['Lyrics']

    # Split text
    all_words = []
    for text in text_column:
        words = text.split()
        all_words.extend(words)

    word_counts = Counter(all_words)

    # Wort finden und Häufigkeit ausgeben
    count = word_counts[word_lower]
    if count > 0:
        st.write(
            f"Das Wort '{word}' ist in {count} Songs enthalten. Damit kommt es in {count / len(text_column) * 100:.0f}% der Songs vor.")
    else:
        st.write(f"Das Wort '{word}' wurde nicht gefunden.")


def explain_stopwords():
    st.subheader("Was sind Stopwords?")
    st. write("Stopwords sind in der Textanalyse und -verarbeitung Wörter, die so häufig vorkommen, dass sie "
              "als wenig aussagekräftig betrachtet werden. Sie tragen in der Regel nicht wesentlich zur Bedeutung "
              "eines Textes bei und werden daher oft aus Texten entfernt, bevor diese weiter analysiert werden.")
    st.write("Beispiele für Stopwords sind Artikel wie _the_ und _a/an_, Pronomen wie _I_ und _you_ sowie Präpositionen "
             "wie _on_, _in_ und _for_ und viele weitere.")

    st.subheader("Warum werden Stopwords entfernt?")
    st.write("Durch das Entfernen dieser Wörter wird die Textmenge kleiner, was die Analyse beschleunigt und effizienter macht."
             " Außerdem kann man sich bei der Analyse so auf die wirklich wichtigen, aussagekräftigen Worte konzentrieren,"
             "die den Inhalt prägen. Weiterhin filtern selbst bekannte Suchmaschinen diese Stopwords in der Regel aus, um "
             "relevantere Sucherergebnisse zu liefern. Hättest du das gewusst?")

############################################################################################################
######                              Most Streamed Songs -- Analyse                                    ######
############################################################################################################

def create_barplot(counter):
    sns.set_style("darkgrid")

    # Erstelle die Figure und Axes
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Plotten der Daten mit grünen Balken
    counter.plot(kind='bar', color='#3d911e', ax=ax, width=0.5)

    # Anpassungen an den Achsen und Beschriftungen
    ax.set_ylabel("Häufigkeit in %", color='white', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelcolor='white', labelsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

    st.pyplot(fig)

############################################################################################################
######                               Korrelationen & Kausalitäten                                     ######
############################################################################################################

def create_corr_matrix(df_numeric):
    # Korrelationsmatrix
    correlation_matrix = df_numeric.corr()

    # Heatmap erstellen
    sns.set_style("darkgrid")

    # Erstelle die Figure und Axes
    fig, ax = plt.subplots(figsize=(20, 15))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    sns.heatmap(correlation_matrix, linewidths=0.1, annot=True, ax=ax, cmap='Greens')
    plt.rcParams.update({'font.size': 9})
    ax.tick_params(axis='both', which='major', labelcolor='white', labelsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.show()

    st.pyplot(fig)


def create_scatterplot(x_axis, y_axis, df_numeric):
    st.scatter_chart(df_numeric, x = x_axis, y = y_axis, color='#3d911e')



############################################################################################################
######                                     Track Database                                             ######
############################################################################################################


def trackdetails(track_input, artist_input, spalte, df):
    track_input = track_input.lower()
    artist_input = artist_input.lower()

    filtered_df = df[(df['Track'].str.contains(track_input, case=False)) & (df['Artist'].str.contains(artist_input, case=False))]

    # Zeige die Ergebnisse an
    if not filtered_df.empty:
        wert = filtered_df[spalte].values[0]
        return wert
    else:
        return "Kein Eintrag gefunden."

############################################################################################################
######                                    Artist Database                                             ######
############################################################################################################

def search_artist(artist_input, df):
    # Konvertiere den Eingabe-Künstlernamen in Kleinbuchstaben für die Suche
    artist_input = artist_input.lower()

    # Konvertiere die "Artist"-Spalte in Kleinbuchstaben für die Suche, speichere aber den Originalwert
    df['artist_lower'] = df['Artist'].str.lower()

    # Filtere den DataFrame nach dem Künstlernamen (in Kleinbuchstaben)
    filtered_df = df[df['artist_lower'] == artist_input]

    return filtered_df['Artist'].iloc[0]

def search_album(artist_input, df):
    # Filtern nach Künstler und alle Alben ausgeben
    filtered_df = df[df['Artist'] == search_artist(artist_input, df)]

    # Entferne Zeilen mit NaN-Werten in der 'Album'-Spalte
    filtered_df = filtered_df.dropna(subset=['Album'])


    if filtered_df.empty:
        st.write("Nicht verfügbar.")
    else:
        unique_albums = list(set(filtered_df['Album']))
        for album in unique_albums:
            st.write(album)

def search_img(artist_input, col, df):
    # Filtern nach Künstler und alle Alben ausgeben
    filtered_df = df[df['Artist'] == search_artist(artist_input, df)]

    # Entferne Zeilen mit NaN-Werten in der 'Album'-Spalte
    filtered_df = filtered_df.dropna(subset=[col])

    if filtered_df.empty:
        st.write("Nicht verfügbar.")
    else:
        unique_imgs = list(set(filtered_df[col]))
        for img in unique_imgs:
            st.image(img)

def search_genre(artist_input, df):
    # Filtern nach Künstler und alle Alben ausgeben
    filtered_df = df[df['Artist'] == search_artist(artist_input, df)]

    # Entferne Zeilen mit NaN-Werten in der 'Album'-Spalte
    filtered_df = filtered_df.dropna(subset=['Genre'])

    if filtered_df.empty:
        st.write("Nicht verfügbar.")
    else:
        unique_list = list(set(filtered_df['Genre']))
        for genre in unique_list:
            st.write(genre)

def search_popularity(artist_input, df):
    # Filtern nach Künstler und alle Alben ausgeben
    filtered_df = df[df['Artist'] == search_artist(artist_input, df)]

    # Entferne Zeilen mit NaN-Werten in der 'Album'-Spalte
    filtered_df = filtered_df.dropna(subset=['Popularity'])

    if filtered_df.empty:
        st.write("Nicht verfügbar.")
    else:
        unique_list = list(set(filtered_df['Popularity']))
        for popularity in unique_list:
            st.write(popularity)