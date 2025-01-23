import streamlit as st
from functions import add_logo, add_sidebar_infos, load_dataset, search_artist, search_album, search_img, search_genre, search_popularity

add_logo()
add_sidebar_infos()

df = load_dataset('data.csv')


streams_spotify = df.groupby('Artist')['Spotify Streams'].sum().sort_values(ascending=False)
streams_pandora = df.groupby('Artist')['Pandora Streams'].sum().sort_values(ascending=False)
streams_soundcloud = df.groupby('Artist')['Soundcloud Streams'].sum().sort_values(ascending=False)

views_yt = df.groupby('Artist')['YouTube Views'].sum().sort_values(ascending=False)
views_tt = df.groupby('Artist')['TikTok Views'].sum().sort_values(ascending=False)



st.title("Artist Database")
st.subheader("Suche hier nach einem Künstler und schau, ob er unter den Most Streamed Songs 2024 ist:")

# Texteingabe
artist_input = st.text_input("Artist:")


if st.button("Artist suchen"):

    st.divider()
    st.header("Allgemeines")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Artist:")
        st.write(search_artist(artist_input, df))
        st.subheader("Genre:")
        search_genre(artist_input, df)
        st.subheader("Popularity:")
        search_popularity(artist_input, df)


    with col2:
        st.subheader("Alben:")
        search_album(artist_input, df)


    with col3:
        search_img(artist_input, 'Artist-Bild', df)

    st.divider()
    st.header("Streams und Views")
    st.divider()

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Spotify:")
        st.write(f"{(streams_spotify.loc[search_artist(artist_input, df)]):,.0f}")
        st.subheader("YouTube Views:")
        st.write(f"{(views_yt.loc[search_artist(artist_input, df)]):,.0f}")


    with col5:
        st.subheader("Pandora:")
        st.write(f"{(streams_pandora.loc[search_artist(artist_input, df)]):,.0f}")
        st.subheader("TikTok Views:")
        st.write(f"{(views_tt.loc[search_artist(artist_input, df)]):,.0f}")


    with col6:
        st.subheader("Soundcloud:")
        st.write(f"{(streams_soundcloud.loc[search_artist(artist_input, df)]):,.0f}")