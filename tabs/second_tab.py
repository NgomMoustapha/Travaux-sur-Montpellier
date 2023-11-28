import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px

title = "Aperçu des données"
sidebar_name = "Aperçu des données"
urlhchl = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_HistoriqueChantiersLineaire.csv"
histo = pd.read_csv(urlhchl, encoding='utf-8', sep=',')
histo = pd.read_csv(urlhchl, encoding='utf-8', sep=',')
histo['debut_chan'] = pd.to_datetime(histo['debut_chan'], format='%Y%m%d', errors='coerce')
histo['fin_chanti'] = pd.to_datetime(histo['fin_chanti'], format='%Y%m%d', errors='coerce')



def run():

    st.title(title)

    st.markdown(
        
        """
        ### Évolution des travaux en métropole

        Ce graphique présente le nombre de chantiers en cours des mois depuis 2016. Il y a également les travaux futurs qui sont déjà prévus mais qui n'ont pas encore débutés.
        
        """
    )

    df=histo
    df['mois_annee_debut'] = df['debut_chan'].dt.to_period('M')
    df['mois_annee_fin'] = df['fin_chanti'].dt.to_period('M')

    date_range = pd.date_range(df['debut_chan'].min(), df['fin_chanti'].max(), freq='MS')
    data_df = pd.DataFrame({'date': date_range})
    data_df['date'].dt.to_period('M')
    # Widget pour la sélection de la nature
    selected_nature = st.multiselect("Sélectionnez la nature", df['nature'].unique(), default=df['nature'].unique())

    # Filtrer les données en fonction de la sélection de l'utilisateur
    filtered_df = df[df['nature'].isin(selected_nature)]

    date_range = pd.date_range(filtered_df['debut_chan'].min(), filtered_df['fin_chanti'].max(), freq='MS')
    data_df = pd.DataFrame({'date': date_range})

    data_df['date'].dt.to_period('M')

    # Utilisez les colonnes 'mois_annee_debut' et 'mois_annee_fin' pour filtrer les occurrences
    occurrences = []
    for _, row in data_df.iterrows():
        mask = (filtered_df['mois_annee_debut'] <= row['date'].to_period('M')) & (filtered_df['mois_annee_fin'] >= row['date'].to_period('M'))
        occurrences.append(len(filtered_df[mask]))

    data_df['occurrences'] = occurrences

    # Créer le graphique avec Plotly en utilisant un diagramme de ligne
    fig = px.line(data_df, x='date', y='occurrences', labels={'x': 'Mois et Année', 'y': 'Nombre d\'occurrences'},
                title=f'Evolution du nombre de chantiers au cours des mois à partir de 2016')

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

    st.markdown(
        """
        ### Distribution des chantiers par prestataires

        Ceci est une distribution qui classe les prestataires selon le nombre de chantiers dont ils sont responsables.

        """
    )

    def process_m_ouvrage(x):
        if isinstance(x, str) and x.startswith('3M'):
            return '3M'
        return x

    # Appliquer la fonction à la colonne 'm_ouvrage'
    df['m_ouvrage'] = df['m_ouvrage'].apply(process_m_ouvrage)

    # Créer un graphique interactif avec Plotly Express
    fig = px.histogram(df, x='m_ouvrage', title='Distribution par prestataire',
                    category_orders={'m_ouvrage': df['m_ouvrage'].value_counts().index})

    # Afficher le graphique avec Streamlit
    st.plotly_chart(fig)

    st.markdown(
        """
        ### Type de travaux

        On observe désormais les types de chantier des plus nombreux et moins nombreux.


        """
    )

        # Créer un graphique interactif avec Plotly Express
    fig = px.histogram(df, x='type', title='Distribution par type de chantier',
                    category_orders={'type': df['type'].value_counts().index})

    # Afficher le graphique avec Streamlit
    st.plotly_chart(fig)
