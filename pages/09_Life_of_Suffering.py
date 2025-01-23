import streamlit
import streamlit as st

st.title("My Life of Suffering")

st.divider()
st.write('Ich wollte ein Tool bauen, das anhand hab Songlyrics — zum Beispiel von einem Songwriter, der gerade ein neues Lied geschrieben hat - vorhersagen kann, ob der Song erfolgreich wird oder nicht.')

st.write('Was ist eigentlich alles schief gegangen? Von A wie "Alles" bis Z wie "Ziemlich viel"…')

st.divider()
st.subheader("Words… don’t come easy…")
st.markdown(":gray[_Words | F. R. David (1981)_]")
st.divider()

st.write('Um die Aufgabe zu lösen, braucht es einen Datensatz mit erfolgreichen Songs. Spotify’s Most Streamed Songs 2024 erschien mir als geeignet. Doch die Sonderzeichen sind die reinste Qual. Nichts half, um die Sonderzeichen vom CSV-Export umzuwandeln. Sie ließen sich auch nicht einfach über „Suchen & Ersetzen“  entfernen, weil es viel zu viele sind. Ohne Umwandlung von Sonderzeichen allerdings auch kein Webscraping...')
st.image('images/sonderzeichen.png', width = 350)
st.write('Also mithilfe von Google Sheets und mehreren Tassen Kaffee die Liste der zu scrapenden Lyrics auf alle Track bis 1 Mrd. Spotify-Streams beschränkt (599 Songs) und manuell alle Sonderzeichen und Tracks entfernt, die nicht Englisch (99 Songs) sind.')

st.markdown('Dann wurde alles durch [LyricsGenius](https://lyricsgenius.readthedocs.io/en/master/) gejagt. Dutzende Fehlermeldungen und 5 Stunden später das Ergebnis: 492 von 500 Texten geladen.')
st.image('images/lyricload.png', width = 350)

st.divider()
st.subheader('Nobody said it was easy, no one ever said it would be this hard…')
st.markdown(":gray[_The Scientist | Coldplay (2002)_]")
st.divider()

st.write('Für eine Ähnlichkeitsanalyse müssen die Lyrics in einzelne Wörter getrennt, um Stopwords und Satzzeichen bereinigt und vektorisiert (TfidfVectorizer) werden. Danach der erste Versuch, geeignete Cluster zu finden. Katastrophe. Elbow-Method und Silhouette zeigen an, dass ein Clustering keinen Sinn macht.')
col1, col2 = st.columns(2)
with col1:
    st.image('images/elbow.png')
with col2:
    st.image('images/silhouette.png')
st.write('Dann der Versuch mit dem LDA-Algorithmus (Latent Dirichlet Allocation). LDA geht davon aus, dass jedes Dokument aus einer Mischung verschiedener Themen besteht. Diese Themen werden durch charakteristische Wörter repräsentiert.LDA kann große Mengen von Texten automatisch in thematische Kategorien einteilen.')
st.write('Klingt super! So richtig eindeutige Themen findet der Algorithmus allerdings nicht. Die Texte ähneln sich zu sehr - oder die Datenmenge zur Analyse ist zu klein.')
st.image('images/lda_modell.png')
st.image('images/lda_topics.png')
st.write('Kann man wenigstens Texte miteinander vergleichen und auf Ähnlichkeit untersuchen? Cosine Similarity sei Dank: Das geht. Für ein Abschlussprojekt aber ein bisschen wenig. Dann analysieren wir eben die Audio-Features. Spotify macht’s möglich…')

st.divider()
st.subheader("The Sound of Silence")
st.markdown(":gray[_Simon & Garfunkel (1970)_]")
st.divider()

st.write('…dachte ich.\nStundenlang habe ich versucht, die API zum Laufen zu bringen. 401 - Zugriff verweigert. Irgendwann habe ich dann die [Mitteilung](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api) gefunden: Am 27. Nov 2024 stellt Spotify die Abfragemöglichkeit der Audio-Features ein. Bumm.')

st.markdown('Eine Nacht drüber geschlafen — denn aufgeben wollte ich immer noch nicht — und nach Alternativen gesucht. [Musicstax](https://musicstax.com/) sieht gut aus. Kurz gefreut, Skript geschrieben, laufen lassen: Fehler. Ein ReCaptcha verhindert den Zugriff, obwohl die robots.txt das Scrapen nicht per se verbietet. StackOverflow und Gemini bemüht um festzustellen: Keine Zeit dafür.')
st.image('images/musicstax.png', width = 300)

st.divider()
st.subheader("But I keep cruisin', Can't stop, won't stop movin'...")
st.markdown(":gray[_Shake it off | Taylor Swift (2014)_]")
st.divider()

st.markdown('Nächster Versuch: [songBPM](https://songbpm.com/). Die Audiofeatures gibt’s teilweise nur in kategorischen Werten, aber hey — besser als nichts. URL geschnappt, Skript angepasst und siehe da: Es läuft! Am Ende tausende(!) 404-Statuscodes, aber einige gehen auch durch.\nProblem: Offenbar wurde irgendwann die URL-Struktur umgestellt. Da das Release-Year ab 2020 abrupt abnimmt… Nun ja. Egal. Ich habe ein paar Daten.')
col3, col4 = st.columns(2)
with col3:
    st.image('images/songbpm1.png')
with col4:
    st.image('images/songbpm2.png')

st.write('Da auch das für eine umfassende Analyse zu wenig sein wird, bemühen wir Spotify um den Rest. Track- und Artist-Foto, Follower und Popularity für eine kleine Database-Abfragemäglichkeit.')

st.markdown('Schnell den Code zusammengebaut und über [spotipy](https://spotipy.readthedocs.io/en/2.25.0/) ausgeführt. Leider konnten auch hier nicht für alle Songs Daten generiert werden. 1243 von 4600 sind wieder deutlich zu wenig Datensätze, um valide Aussagen über Korrelationen und Schlussfolgerungen zu treffen.')
st.image('images/spotify.png', width = 350)

st.divider()
st.subheader('This is the end, you know…')
st.markdown(":gray[_Fairytale Gone Bad | Sunrise Avenue (2006)_]")
st.divider()

st.write('Am Ende entsteht hier ein kleines aber feines Tool zur Analyse von Songtexten und ihrer Vergleichbarkeit mit den am häufigsten gestreamten Songs 2024 und einer Track- und Artist-Datenbank mit umfangreichen Informationen zu den Künstlern und ihren Songs.')

st.write('Viel Spaß beim Ausprobieren!')

# Titelbild
st.markdown("""
<div style="text-align: center;">
  <img src="https://i.imgur.com/F3tDM34.png" alt="Mein Logo">
</div>
""", unsafe_allow_html=True)

