import streamlit as st
from functions import add_logo, add_sidebar_infos, load_dataset, trackdetails, search_img


add_logo()
add_sidebar_infos()


df = load_dataset('data.csv')

st.title("Track Database")
st.subheader("Suche hier nach einem Song und schau, ob er zu den Most Streamed Songs 2024 gehört:")

# Texteingabe
track_input = st.text_input("Track:")
artist_input = st.text_input("Artist:")


if st.button("Track suchen"):

    st.divider()
    st.header("Allgemeines")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Titel:")
        st.write(trackdetails(track_input, artist_input, 'Track', df))
        st.subheader("Release Year:")
        st.write(trackdetails(track_input, artist_input, 'Release Year', df))
        st.subheader("Explicit Track:")
        st.write(trackdetails(track_input, artist_input, 'Explicit Track', df))


    with col2:
        st.subheader("Interpret:")
        st.write(trackdetails(track_input, artist_input, 'Artist', df))
        st.subheader("Album:")
        st.write(trackdetails(track_input, artist_input, 'Album', df))
        st.subheader("Popularity:")
        st.write(f"{(trackdetails(track_input, artist_input, 'Spotify Popularity', df)):,.0f}")

    with col3:
        search_img(artist_input, 'Track-Bild', df)

    st.divider()
    st.header("Streams")
    st.divider()

    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("Spotify:")
        st.write(f"{(trackdetails(track_input, artist_input, 'Spotify Streams', df)):,.0f}")
        st.subheader("YouTube Views:")
        st.write(f"{(trackdetails(track_input, artist_input, 'YouTube Views', df)):,.0f}")

    with col5:
        st.subheader("Pandora:")
        st.write(f"{(trackdetails(track_input, artist_input, 'Pandora Streams', df)):,.0f}")
        st.subheader("TikTok Views:")
        st.write(f"{(trackdetails(track_input, artist_input, 'TikTok Views', df)):,.0f}")

    with col6:
        st.subheader("Soundcloud:")
        st.write(f"{(trackdetails(track_input, artist_input, 'Soundcloud Streams', df)):,.0f}")
        st.subheader("All Time Rank:")
        st.write(f"{(trackdetails(track_input, artist_input, 'All Time Rank', df)):,.0f}")

    st.divider()
    st.header("Audio-Features")
    st.divider()

    col7, col8, col9 = st.columns(3)

    with col7:
        st.subheader("Tempo in BPM:")
        st.write(trackdetails(track_input, artist_input, 'Tempo', df))
        st.subheader("Stimmung:")
        st.write(trackdetails(track_input, artist_input, 'Stimmung', df))

    with col8:
        st.subheader("Tonart:")
        st.write(trackdetails(track_input, artist_input, 'Key', df), trackdetails(track_input, artist_input, 'Mode', df))
        st.subheader("Energy:")
        st.write(trackdetails(track_input, artist_input, 'Energy', df))

    with col9:
        st.subheader(" ")
        st.markdown("""<span style='color:black'>leer</span>""", unsafe_allow_html=True)
        st.subheader("Danceability:")
        st.write(trackdetails(track_input, artist_input, 'Danceability', df))