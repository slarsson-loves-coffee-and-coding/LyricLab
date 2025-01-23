import streamlit as st
from functions import add_logo, add_sidebar_infos, load_dataset, create_barplot

add_logo()
add_sidebar_infos()

df = load_dataset('data.csv')
df["Track_lower"] = df['Track'].str.lower()
df = df.drop_duplicates(subset='Track_lower')
df = df.drop(["Track_lower"], axis = 1)


st.title("Most Streamed Songs auf Spotify 2024 - Die Analyse")
st.divider()

st.header("Die Songs und Interpreten")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("Welche 10 Artists sind mit den meisten Songs vertreten?")
    st.write(df['Artist'].value_counts().nlargest(10))

with col2:
    st.write("Welche 10 Alben sind sind am häufigsten in der Top-Liste?")
    st.write(df['Album'].value_counts().nlargest(10))

st.subheader("Welche Künstler haben die meisten Follower auf Spotify?")

most_followers = df.groupby('Artist')['Follower'].sum().sort_values(ascending=False).head(3)
st.write(most_followers)

st.divider()

st.header("Streams und Views")

st.divider()

st.subheader("Welche sind die meistgestreamten Songs?")

st.write("Spotify:")
meistgestreamte = df.sort_values('Spotify Streams', ascending=False).head(3)
st.write(meistgestreamte[['Track', 'Artist', 'Spotify Streams']])

st.write("Pandora:")
meistgestreamte = df.sort_values('Pandora Streams', ascending=False).head(3)
st.write(meistgestreamte[['Track', 'Artist', 'Pandora Streams']])

st.write("Soundcloud:")
meistgestreamte = df.sort_values('Soundcloud Streams', ascending=False).head(3)
st.write(meistgestreamte[['Track', 'Artist', 'Soundcloud Streams']])


st.subheader("Welche Songs haben die meisten Views?")

st.write("YouTube:")
meiste_likes = df.sort_values('YouTube Views', ascending=False).head(3)
st.write(meiste_likes[['Track', 'Artist', 'YouTube Views']])

st.write("TikTok:")
meiste_likes = df.sort_values('TikTok Views', ascending=False).head(3)
st.write(meiste_likes[['Track', 'Artist', 'TikTok Views']])

###################################################

st.subheader("In welchem Jahr sind die meisten erfolgreichen Songs erschienen?")
st.caption(f"in Prozent | Basis: {df['Release Year'].count()} Songs")
col3, col4 = st.columns([2, 3])
with col3:
    year = df['Release Year'].value_counts(normalize=True) * 100
    year = year.head(10).round(0)
    st.write(year)

with col4:
    create_barplot(year)

st.subheader("Welche sind die drei ältesten Songs?")

aelteste_tracks = df.sort_values('Release Year').head(3)
st.write(aelteste_tracks[['Track', 'Artist', 'Release Year']])




###################################################

st.subheader("In welchem Land sind die meisten erfolgreichen Songs erschienen?")
st.caption(f"in Prozent | Basis: {df['Release Country'].count()} Songs")
col5, col6 = st.columns([0.33, 0.66])
with col5:
    country = df['Release Country'].value_counts(normalize=True) * 100
    country = country.head(10).round(0)
    st.write(country)
with col6:
    create_barplot(country)
    st.markdown("Anmerkung: QZ und QM gehören ebenfalls zu den US.\nMehr Infos dazu [hier.](https://isrc.ifpi.org/downloads/Valid_Characters.pdf)")
###################################################

st.subheader("Wie viele Songs sind Explicit?")
st.caption(f"in Prozent | Basis: {df['Explicit Track'].count()} Songs")
col7, col8 = st.columns([0.33, 0.66])
with col7:
    explicit = df['Explicit Track'].value_counts(normalize=True) * 100
    explicit = explicit.round(0)
    st.write(explicit)
with col8:
    create_barplot(explicit)

st.divider()

st.header("Die Audio-Features")

st.divider()

###################################################

st.subheader("Wie ist die Stimmung der Tracks?")
st.caption(f"in Prozent | Basis: {df['Stimmung'].count()} Songs")
col9, col10 = st.columns([0.33, 0.66])
with col9:
    stimmung = df['Stimmung'].value_counts(normalize=True) * 100
    stimmung = stimmung.round(0)
    st.write(stimmung)
with col10:
    create_barplot(stimmung)

###################################################

###################################################

st.subheader("Welche Tonart kommt am häufigsten vor?")
st.caption(f"in Prozent | Basis: {df['Mode'].count()} Songs")
col13, col14 = st.columns([0.33, 0.66])
with col13:
    mode = df['Mode'].value_counts(normalize=True) * 100
    mode = mode.round(0)
    st.write(mode)
with col14:
    create_barplot(mode)

###################################################

st.subheader("Wie energiegeladen sind die Tracks?")
st.caption(f"in Prozent | Basis: {df['Energy'].count()} Songs")
col15, col16 = st.columns([0.33, 0.66])
with col15:
    energy = df['Energy'].value_counts(normalize=True) * 100
    energy = energy.round(0)
    st.write(energy)
with col16:
    create_barplot(energy)

###################################################

st.subheader("Wie tanzbar sind die Songs?")
st.caption(f"in Prozent | Basis: {df['Danceability'].count()} Songs")
col17, col18 = st.columns([0.33, 0.66])
with col17:
    dance = df['Danceability'].value_counts(normalize=True) * 100
    dance = dance.round(0)
    st.write(dance)
with col18:
    create_barplot(dance)

###################################################

st.subheader("Welcher ist der meistgewählte Takt?")
st.caption(f"in Prozent | Basis: {df['Beats per Bar'].count()} Songs")
col19, col20 = st.columns([0.33, 0.66])
with col19:
    beats = df['Beats per Bar'].value_counts(normalize=True) * 100
    beats = beats.round(0)
    st.write(beats)
with col20:
    create_barplot(beats)
