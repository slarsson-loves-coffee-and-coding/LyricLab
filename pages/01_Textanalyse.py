import streamlit as st
import pandas as pd
from functions import add_logo, add_sidebar_infos, create_wordcloud,print_wordlist, search_word, explain_stopwords

add_logo()
add_sidebar_infos()
df = pd.read_csv('spotify-data_lyrics.csv')


# Streamlit App
st.title("Die beliebtesten Wörter")
st.write("Welche Wörter werden am häufigsten in Songtexten genutzt? Lässt sich ein Muster erkennen? Finde es heraus!")


tab1, tab2, tab3 = st.tabs(["Wortwolke", "Liste", "Wortsuche"])

# Inhalt für Tab 1
with tab1:
    st.subheader("Die häufigsten Wörter als Wortwolke")
    fig = create_wordcloud()
    st.pyplot(fig)
    st.caption(f"Die häufigsten Wörter in {df['Lyrics'].count()} analysierten Songs (bereinigt um Stopwords).")
    st.divider()
    explain_stopwords()



# Inhalt für Tab
with tab2:
    st.subheader("Wortlisten-Generator")
    num_words = st.slider("Anzahl der häufigsten Wörter:", min_value=1, max_value=200, value=100)

    if st.button("Wortliste erstellen"):
        df= pd.read_csv('spotify-data_lyrics.csv')
        print_wordlist(num_words)
        st.divider()
        st.caption(f"Die {num_words} häufigsten Wörter in {df['Lyrics'].count()} analysierten Songs bereinigt um Stopwords.")



# Inhalt für Tab
with tab3:
    # Streamlit App
    st.subheader("Wort suchen")
    st.write("Du suchst ein bestimmtes Wort und möchtest wissen, in wie vielen Songs es vorkommt?")

    word = st.text_input("Gib hier das gesuchte Wort* ein:")
    if st.button("Wort suchen"):
        search_word(word)
        st.caption("*Das Wort sollte aus der Englischen Sprache sein und nicht zu den Stopwords gehören.")
        st.divider()
        explain_stopwords()