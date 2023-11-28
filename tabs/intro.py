import streamlit as st


title = "Chantiers dans la métropole de Montpellier"

sidebar_name = "Introduction"


def run():

    st.image("assets/sheldon.gif")


    st.title(title)

    st.markdown("----")

    st.markdown(
        """
       Ce site a pour but de présenter de manière synthétique les chantiers en cours sur l'ensemble de la métropole montpelliéraine.
       L'objectif est d'observer dans quelle mesure les travaux impactent la circulation et la vie en générale à Montpellier.
       Des graphiques sont présents dans la rubrique Aperçu des données pour avoir quelques détails sur les chantiers et une carte intéractive permet à l'utilisateur d'avoir une visualisation géographique de la situation 
       actuelle des travaux de la métropole dans la rubrique Carte.
        """
    )





                


