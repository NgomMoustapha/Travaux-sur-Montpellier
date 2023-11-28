import streamlit as st
import requests
from datetime import datetime
from shapely.geometry import Polygon
import folium
from folium.plugins import MarkerCluster
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import requests
from datetime import datetime
from shapely.geometry import Polygon

title = "Chantiers dans la métropole de Montpellier"

sidebar_name = "Introduction"


def run():

    st.image("/home/moustapha/Desktop/OpenData/streamlit_app/assets/sheldon.gif")


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

    def carte_traveaux():
        url_chant = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_HistoriqueChantiersPoint.json"
        url_chantgen = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_ChantiersGenantsPoints.json"

        icon_create_function = """\
        function(cluster) {
            return L.divIcon({
                html: '<div style="text-align: center; padding-top: 8px;"><b>' + cluster.getChildCount() + '</b></div>',
                className: 'marker-cluster marker-cluster-large',
                iconSize: new L.Point(40, 40)
            });
        }
        """

        ma_carte = folium.Map(location=[43.62505, 3.862038], zoom_start=10.5) 

        response_chant = requests.get(url_chant)
        data_chant = response_chant.json()

        response_chantgen = requests.get(url_chantgen)
        data_chantgen = response_chantgen.json()

        aujourdhui = datetime.now().strftime('%Y%m%d')
        travaux_en_cours_chant = []

        for feature in data_chant['features']:
            debut_chantier_str = feature['properties']['debut_chan']
            fin_chantier_str = feature['properties']['fin_chanti']

            debut_chantier = datetime.strptime(debut_chantier_str, '%Y%m%d').strftime('%Y%m%d')
            fin_chantier = datetime.strptime(fin_chantier_str, '%Y%m%d').strftime('%Y%m%d')

            if debut_chantier <= aujourdhui <= fin_chantier:
                travaux_en_cours_chant.append(feature)

        travaux_en_cours_chantgen = []

        chantgen_ids = {feature['properties']['numero'] for feature in data_chantgen['features']}

        for feature in travaux_en_cours_chant:
            chant_id = feature['properties']['numero_fic']
            
            if chant_id in chantgen_ids:
                feature['chantgen'] = True
            else:
                feature['chantgen'] = False
            
            travaux_en_cours_chantgen.append(feature)

        marker_cluster = MarkerCluster(icon_create_function=icon_create_function).add_to(ma_carte)

        for feature in travaux_en_cours_chantgen:
            coordinates = feature['geometry']['coordinates']
            properties = feature['properties']
            popup_content = f"<b>Adresse :</b> '{properties.get('adresse', 'N/A')}'<br><b>Type de travaux :</b> '{properties.get('type', 'N/A')}'<br><b>Prestataire :</b> '{properties.get('m_ouvrage', 'N/A')}'"
            popup = folium.Popup(popup_content, max_width=600)  

            if feature.get('chantgen'):
                icon_path = "/home/moustapha/Desktop/OpenData/streamlit_app/assets/img_rouge.png"  
            else:
                icon_path = "/home/moustapha/Desktop/OpenData/streamlit_app/assets/img.png" 

            icon = folium.CustomIcon(icon_image=icon_path, icon_size=(30, 30))
            folium.Marker(location=[coordinates[1], coordinates[0]], popup=popup, icon=icon).add_to(marker_cluster)

        url_lineaire = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_HistoriqueChantiersLineaire.json"

        response_lineaire = requests.get(url_lineaire)
        data_lineaire = response_lineaire.json()

        travaux_en_cours_lineaire = []

        for feature in data_lineaire['features']:
            debut_chantier_str = feature['properties']['debut_chan']
            fin_chantier_str = feature['properties']['fin_chanti']

            debut_chantier = datetime.strptime(debut_chantier_str, '%Y%m%d').strftime('%Y%m%d')
            fin_chantier = datetime.strptime(fin_chantier_str, '%Y%m%d').strftime('%Y%m%d')

            if debut_chantier <= aujourdhui <= fin_chantier:
                travaux_en_cours_lineaire.append(feature)

        data_lineaire = travaux_en_cours_lineaire

        polygons = []

        for feature in data_lineaire:
            geometry = feature.get('geometry') 
            
            if geometry:
                geom_type = geometry['type']
                coordinates = []

                if geom_type == 'Polygon':
                    coordinates = geometry['coordinates'][0]
                elif geom_type == 'MultiPolygon':
                    multi_coords = geometry['coordinates']
                    for poly_coords in multi_coords:
                        coordinates.extend(poly_coords[0])

                if coordinates:
                    formatted_coords = [(coord[1], coord[0]) for coord in coordinates]
                    
                    
                    polygon_color = 'red' if feature['properties']['numero_fic'] in chantgen_ids else '#ff7900'

                    polygons.append((formatted_coords, polygon_color))

        for coords, color in polygons:
            folium.Polygon(locations=coords, color=color, fill=True, fill_color=color, fill_opacity=0.4).add_to(ma_carte)
        return ma_carte
    
    folium_static(carte_traveaux())
    




                


