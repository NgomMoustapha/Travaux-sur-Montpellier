import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import requests
from datetime import datetime
from shapely.geometry import Polygon

title = "Carte"
sidebar_name = "Carte"


def run():

    st.title(title)

    st.markdown(
        """
        This is the third sample tab.
        """
    )



    # Fonction pour créer l'icône du cluster
    icon_create_function = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="text-align: center; padding-top: 8px;"><b>' + cluster.getChildCount() + '</b></div>',
            className: 'marker-cluster marker-cluster-large',
            iconSize: new L.Point(40, 40)
        });
    }
    """

    st.markdown(
        """
        polygone
        """
    )

    # URL des données JSON
    url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_HistoriqueChantiersPoint.json"

    # Charger les données JSON
    response = requests.get(url)
    data = response.json()

    # Obtenez la date actuelle au format YYYYMMDD
    aujourdhui = datetime.now().strftime('%Y%m%d')

    # Liste pour stocker les travaux en cours
    travaux_en_cours = []

    # Parcourez chaque feature dans la liste des features
    for feature in data['features']:
        debut_chantier_str = feature['properties']['debut_chan']
        fin_chantier_str = feature['properties']['fin_chanti']

        # Convertissez les chaînes de date en objets de date
        debut_chantier = datetime.strptime(debut_chantier_str, '%Y%m%d').strftime('%Y%m%d')
        fin_chantier = datetime.strptime(fin_chantier_str, '%Y%m%d').strftime('%Y%m%d')

        # Vérifiez si le chantier est en cours à la date d'aujourd'hui
        if debut_chantier <= aujourdhui <= fin_chantier:
            travaux_en_cours.append(feature)

    # Créez une carte Folium
    ma_carte = folium.Map(location=[43.62505, 3.862038], zoom_start=8)

    # Utilisez le module MarkerCluster pour regrouper les marqueurs
    marker_cluster = MarkerCluster(icon_create_function=icon_create_function).add_to(ma_carte)

    # Ajoutez les marqueurs à la carte
    for feature in travaux_en_cours:
        coordinates = feature['geometry']['coordinates']
        properties = feature['properties']
        popup_content = f"<b>Adresse :</b> '{properties.get('adresse', 'N/A')}'<br><b>Type de travaux :</b> '{properties.get('type', 'N/A')}'<br><b>Prestataire :</b> '{properties.get('m_ouvrage', 'N/A')}'"
        popup = folium.Popup(popup_content, max_width=600)  # Changer la largeur maximale

        # Utilisez le module CustomIcon pour personnaliser l'icône du marqueur
        icon = folium.CustomIcon(icon_image='/home/moustapha/Desktop/OpenData/streamlit_app/assets/img.png', icon_size=(30, 30))
        folium.Marker(location=[coordinates[1], coordinates[0]], popup=popup, icon=icon).add_to(marker_cluster)



    # Fonction pour créer l'icône du cluster
    icon_create_function = """\
    function(cluster) {
        return L.divIcon({
            html: '<div style="text-align: center; padding-top: 8px;"><b>' + cluster.getChildCount() + '</b></div>',
            className: 'marker-cluster marker-cluster-large',
            iconSize: new L.Point(40, 40)
        });
    }
    """

    # URL des données JSON
    url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_HistoriqueChantiersLineaire.json"

    # Télécharger le contenu JSON depuis l'URL
    response = requests.get(url)
    data = response.json()

    # Obtenez la date actuelle au format YYYYMMDD
    aujourdhui = datetime.now().strftime('%Y%m%d')

    # Liste pour stocker les travaux en cours
    travaux_en_cours = []

    # Parcourez chaque feature dans la liste des features
    for feature in data['features']:
        debut_chantier_str = feature['properties']['debut_chan']
        fin_chantier_str = feature['properties']['fin_chanti']

        # Convertissez les chaînes de date en objets de date
        debut_chantier = datetime.strptime(debut_chantier_str, '%Y%m%d').strftime('%Y%m%d')
        fin_chantier = datetime.strptime(fin_chantier_str, '%Y%m%d').strftime('%Y%m%d')

        # Vérifiez si le chantier est en cours à la date d'aujourd'hui
        if debut_chantier <= aujourdhui <= fin_chantier:
            travaux_en_cours.append(feature)


    # Utilisez le module MarkerCluster pour regrouper les marqueurs
    marker_cluster = MarkerCluster(icon_create_function=icon_create_function).add_to(ma_carte)

    # Liste pour stocker les polygones
    polygons = []

    # Parcourir les features du fichier JSON et extraire les coordonnées des Polygons et Multipolygons
    for feature in travaux_en_cours:
        geometry = feature.get('geometry')  # Utiliser get() pour éviter les valeurs None

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
                polygons.append(formatted_coords)

    # Ajouter chaque polygone à la carte
    for coords in polygons:
        # Convertir les coordonnées en objets Polygon
        poly = Polygon(coords)

        # Récupérer les coordonnées pour tracer le polygone sur la carte
        coords = list(poly.exterior.coords)

        # Tracer le polygone sur la carte
        folium.Polygon(locations=coords, color='blue', fill=True, fill_color='blue', fill_opacity=0.4).add_to(marker_cluster)

    # Affichez la carte dans Streamlit
    folium_static(ma_carte)


