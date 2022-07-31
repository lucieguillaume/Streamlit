# pip install streamlit-aggrid
# pip install plotly --upgrade

import pandas as pd 
import plotly.express as px 
import streamlit as st
st.set_page_config(layout="wide") # Mettre la page en mode élargie

#Import du jeu de données 
df = pd.read_csv('/Users/lucel/OneDrive/Documents/streamlit/spotify.csv')
df_clean = df.loc[df['year'] > 2010] # Suppression de 4 titres pour améliorer le rendus des graphiques

# Création titre et sous titre
st.title("Dashboard : Spotify")
st.markdown("À l'aide des données de la playlist 'Top 100 most streamed' sur Spotify, découvrons si les tendances musicales actuelles peuvent nous aider à créér le hit de demain ?")
st.markdown("_____________________________________________________")

# Création de la sidebar
st.sidebar.image("/Users/lucel/OneDrive/Documents/streamlit/logo2.png",width=190)
st.sidebar.title("...")
st.sidebar.subheader("🏠 Accueil")
st.sidebar.subheader("🔎 Rechercher")
st.sidebar.subheader("📚 Biliothèque ")
st.sidebar.subheader("")
st.sidebar.subheader("➕ Créer une playlist")
st.sidebar.subheader("💟 Titres likés")
st.sidebar.markdown("_________________")
st.sidebar.subheader("Travelling")
st.sidebar.subheader("Good vibes")
st.sidebar.subheader("Sad songs")
st.sidebar.subheader("70s Road Trip")

# Import du fichier audio
audio_file = open("/Users/lucel/OneDrive/Documents/streamlit/surprise.wav",'rb')
audio_bytes = audio_file.read()
# Ajout du lecteur à la sidebar
st.sidebar.audio(audio_bytes)

# Création de la structure du dashboard en 2 colonnes
left_block, right_block = st.columns([1,1])

# Définition du premier bloc
with left_block: 

    # Définition du premier container
    first_container = st.container()

    with first_container: 
        
        # 1 - Top 5 genres / artistes 

        # Créer une fonction qui prend en paramètre l'option du bouton radio selectionnée
        def generate_chart(select):

            if select == 'Genres': #Cas où on sélectionne Genre
                df_genre = pd.DataFrame(df['top genre'].value_counts())
                df_genre.columns = ["Nombre de morceaux"] #Je renomme la colonne des valeurs "Nombre de morceaux"
                df_genre = df_genre.rename_axis("Genre").reset_index()#Je reset l'index et je nomme ma première colonne Genre
                df_genre = df_genre.iloc[0:5] #Je garde les 5 premiers

                #Je paramètre ma figure
                fig = px.pie(df_genre, names="Genre", 
                values="Nombre de morceaux",
                title="TOP 5 des genres musicaux", 
                color_discrete_sequence=px.colors.sequential.Plasma)

                fig.update_traces(textposition='inside', 
                textinfo='percent+label', 
                textfont_size=12, 
                textfont_color='white', 
                showlegend=False)

                #J'affiche mon titre au centre et en taille 18
                fig.update_layout(title_x = 0.5, font=dict(size=18))
    
            else: #Cas où on sélectionne Artistes
                df_artist = pd.DataFrame(df['artist'].value_counts()) 
                df_artist.columns = ["Nombre de morceaux"] #Je renomme la colonne des valeurs "Nombre de morceaux"
                df_artist = df_artist.rename_axis("Nom de l'artiste").reset_index() #Je reset l'index et je nomme ma première colonne Nom de l'artiste
                df_artist = df_artist.iloc[0:5] #Je garde les 5 premiers

                # Je paramètre ma figure
                fig = px.pie(df_artist, 
                names="Nom de l'artiste", 
                values="Nombre de morceaux", 
                title="TOP 5 des artistes", 
                color_discrete_sequence=px.colors.sequential.thermal)

                fig.update_traces(textposition='inside', 
                textinfo='percent+label', 
                textfont_size=13, 
                textfont_color='white', 
                showlegend=False)

                #J'affiche mon titre au centre et en taille 25
                fig.update_layout(title_x = 0.5, font=dict(size=25))

            return st.plotly_chart(fig, use_container_width=True,config={'displayModeBar':False})

    # Création du boutton radio pour alterner entre les 2 graphiques
    select = st.radio('Choisir variable :', ('Genres', 'Artistes'))

    # Générer le graphique
    generate_chart(select)

    # Création d'un expander d'explication des résultats
    with st.expander("Voir l'explication"):
        
        st.markdown("""
        1. Conclusion Artistes : 
        
        Nous pouvons voir que Post Malone a 7 chansons dans le top 10, Ed Sheeran en a 5, puis The Weekend et Imagine Draongs en ont 4. 
        
        Les autres artistes de ce top ont moins de 3 chansons.
        
        2. Conclusion Genre : 
        
        Nous pouvons voir que la dance pop est très largement représentée à 48.3%, suivi par la pop à 19%, et Dallas-Fort Worth/Arlington (DFW Rap) à 12%""")  

    # Définition du deuxième container
    second_container = st.container()
    
    with second_container:

        # 2 - Durée moyenne des morceaux en fonction de l'année

        duree_annee = df_clean[["length", "year", "title"]].groupby(by=["year"]).agg("mean") 
        duree_annee['length'].round(2) #J'arrondi à 2 chiffres après la virgule la durée
        duree_annee.reset_index(inplace=True)

        #Je paramètre ma figure
        fig2 = px.line(duree_annee, 
        x="year", 
        y="length", 
        title="Durée moyenne des morceaux en fonction de l'année",
        labels={'year':'Année de sortie du morceau', 'length':'Durée du morceau (en seconde)'}, 
        markers=True,
        color_discrete_sequence=["orange"],
        range_x=[2011,2022])

        fig2.add_annotation(x=2021, y=167.33,
        text="2 min 47",
        showarrow=True,
        arrowhead=1,
        font=dict(
        family="Courier New, monospace",
        size=14,
        color="#ffffff"),
        align="center",
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=1)

        fig2.add_annotation(x=2013, y=256.73,
        text="4 min 16",
        showarrow=True,
        arrowhead=1,
        font=dict(
        family="Courier New, monospace",
        size=14,
        color="#ffffff"),
        align="center",
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=20,
        ay=-30,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=4,
        bgcolor="#ff7f0e",
        opacity=1)

        #J'affiche le titre au centre et en taille 17
        fig2.update_layout(title_x = 0.5, font=dict(size=17))

        #J'affiche mon graphique
        st.plotly_chart(fig2, use_container_width=True,config={'displayModeBar':False}) #Affichage du graphique

        # Création d'un expander d'explication des résultats
        with st.expander("Voir l'explication"): 
            
            st.markdown(""" 
            
            On peut voir une chute vertigineuse de la durée des morceaux au cours du temps 

            Le streaming a totalement changé la manière de consommer la musique. 
            
            Quand en 2013 on observe une durée moyenne de 4'16, en 2021 les morceaux ne durent plus que 2'47 en moyenne
            
            """)

with right_block:    
    
    #Je créé mon troisième container
    third_container = st.container() 

    with third_container:

        # 3 - Graphique en barres de la moyenne de chaque indicateur / artiste

        #Je ne garde que les valeurs uniques
        select_artist = df["artist"].drop_duplicates()
        
        #Je créé mon selectbox
        list_artist = st.selectbox("Choisir artiste :",select_artist) 
        
        df_object = df_clean.drop(['year','top genre','title','loudness.dB','length','beats.per.minute'], axis=1)
        df3 = df_object.groupby("artist").agg("mean")
        df4 = pd.DataFrame(df_object.agg("mean"))
        df4.columns = ["Valeurs"]
        df4 = df4.rename_axis('Variables').reset_index().sort_values(by="Valeurs",ascending=False)

        # df4 = df3.query("artist in @list_artist") # Pas réussi

        # df4 

        # Je paramètre ma figure 
        fig3 = px.bar(df4, x="Valeurs", 
        y="Variables",
        title = "Valeurs moyennes / attribut ", 
        text="Valeurs", 
        hover_data=['Variables', 'Valeurs'], 
        labels={'Valeurs':'Moyenne', 
        'Variables':'Attributs'},
        orientation ='h',
        color="Variables",
        color_discrete_sequence=px.colors.sequential.Plasma)

        fig3.update_traces(texttemplate='%{text:.2s}', 
        textposition='inside', 
        textfont_color='white', 
        showlegend=False) 
        
        #Ne pas afficher la grille en x
        fig3.update_xaxes(showgrid=False)

        #Centrer le litre et l'afficher en taille 18
        fig3.update_layout(title_x = 0.5, font=dict(size=18))
        
        # Je print ma figure
        st.plotly_chart(fig3, use_container_width=True,config={'displayModeBar':False})

        # Création d'un expander d'explication des résultats
        with st.expander("Voir l'explication"): 
            
            st.markdown("""
        
        D'après ce graphique, le top 100 des chansons Spotify se caractérise par :

        * une popularité très élevée : 80
        
        * une capacité à faire danser et une énergie plutôt élevée : > 60
        
        * peu de paroles : speechiness de 10
        
        * globalement des musiques enregistrées en studio : liveness de 17
        
        """)  

    #Je créé mon quatrième container 
    fourth_container = st.container()
    
    with fourth_container:

        # 4 - Valance moyenne des morceaux en fonction de la popularité

        valance_popularite = df_clean[["valance", "popularity", "title"]].groupby(by=["popularity"]).agg("mean").sort_values(by="popularity",ascending=False)

        valance_popularite.reset_index(inplace=True)

        # Je paramètre ma figure 
        fig5 = px.bar(valance_popularite, 
        x="popularity", 
        y="valance", 
        title="Valance moyenne des morceaux en fonction de la popularité",
        color='popularity',
        labels={'popularity':'Popularité', 'valance':'Valance'},
        range_x=[65,92])

        # J'affiche le titre au centre et en taille 17
        fig5.update_layout(title_x = 0.5, font=dict(size=17))

        # Je print ma figure
        st.plotly_chart(fig5, use_container_width=True,config={'displayModeBar':False})

        # Création d'un expander d'explication des résultats
        with st.expander("Voir l'explication"):
            
            st.markdown("""
            
            D'après ce graphique, on remarque que la valance n'a pas de relation avec la popularité. 
            
            Une musique plus joyeuse n'est pas forcément plus populaire.
            
            """)




