import pandas as pd 
import plotly.express as px 
import streamlit as st


df = pd.read_csv('spotify.csv')


st.title("Le jeu de données")
st.write("Données brutes")
df

st.write("Tableau de corrélation")
string = ["title", "artist", "top genre"]
corr = df.drop(columns=string).corr()
corr 

st.caption('This is a string that explains something above.')