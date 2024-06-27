import streamlit as st
import pandas as pd
import plost
import plotly.express as px
import streamlit_authenticator as stauth 
import pyodbc
from streamlit_option_menu import option_menu
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import json
from streamlit_lottie import st_lottie
import requests
from wordcloud import STOPWORDS
import nltk
import warnings
import plotly.graph_objects as go
import altair as alt
import os
warnings.filterwarnings('ignore')

# Crea la cadena de conexión sin usuario y contraseña (usando la autenticación de Windows)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# # Ruta del archivo JSON con las credenciales
# credentials_file = 'genial-bonbon-427315-j6-7fdf1ca74270.json'

# # Autenticar y crear un cliente
# sa = gspread.service_account(st.secrets["gcp_service_account"])
# sh = sa.open("desaparecidosdb")

# # Seleccionar la hoja (worksheet)
# wks = sh.worksheet('Hoja 1')

# # Obtener todos los registros
# records = wks.get_all_records()

# # Convertir los registros a un DataFrame de pandas
# df = pd.DataFrame.from_records(records)

file_path = "desaparecidosdb3.xlsx"
df = pd.read_excel(file_path)


df['estatura'] = pd.to_numeric(df['estatura'], errors='coerce')
df['horas_para_aparecer'] = pd.to_numeric(df['horas_para_aparecer'], errors='coerce')
df['horas_para_denunciar'] = pd.to_numeric(df['horas_para_denunciar'], errors='coerce')
df['aparecido'] = pd.to_numeric(df['aparecido'], errors='coerce')



## configuración del side bar
# Configuration of the side bar
st.set_page_config(
    page_title="Los Saqueadores",
    page_icon=":skull:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
.header {
    font-family: 'Roboto', sans-serif;
    text-align: center;
    color: #FF6F61;  /* Coral color */
    padding: 0px;
    margin-bottom: 40px;  /* Add spacing after the title */
}
.content {
    font-family: 'Roboto', sans-serif;
    color: white;
    margin-top: 30px;
    margin-left: 20px;
    padding-left: 0px;
}
.embed-container {
    position: auto;
    margin-top: -30px;
    padding-bottom: 500px;
    height: 0;
    overflow: hidden;
    max-width: 35%;
    height: 35%;
}
.embed-container iframe {
    position: absolute;
    top: 50%;  /* Scroll to the middle */
    left: 0;
    width: 100%;
    height: 100%;
    transform: translateY(-45%);  /* Adjust for centering */
}
</style>
""", unsafe_allow_html=True)

import streamlit as st
import os

# Correct the image path
image_path = os.path.join(os.path.dirname(__file__), 'images', 'saqueadoreslogo.png')

# Ensure the file exists
if os.path.exists(image_path):
    st.sidebar.image(image_path, use_column_width=True)
else:
    st.sidebar.error(f"Image file not found: {image_path}")

st.sidebar.markdown("<h1 class='sidebar-title' style='text-align:center;'>Los Saqueadores</h1>", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Busqueda de Personas", "Dashboard", "Apriori", "Random Forest","Clusters","ARIMA"],
        icons=["house", "person-fill", "coin", "book", "person-fill", "book", "person-fill"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.markdown("<h1 class='header'>Centro de Información de Personas Desaparecidas</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="embed-container">
                <iframe src="https://desaparecidosenperu.policia.gob.pe" frameborder="0" allowfullscreen></iframe>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='content' style='font-size: 18px; padding-bottom: 30px;'>Proyecto que busca dar visibilidad y trazabilidad a las personas desaparecidas en Perú. Se hace uso de datos del RENIPED actualizados diariamente para un análisis y predicción de estos.</div>", unsafe_allow_html=True)
        # Correct the image path
        image_path = os.path.join(os.path.dirname(__file__), 'images', 'desap.png')

        # Ensure the file exists
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.error(f"Image file not found: {image_path}")

        with st.expander('About', expanded=True):
            st.write('''
                - Datos: [Historico 2024](https://desaparecidosenperu.policia.gob.pe/WebDesaparecidos/documento/2024.xlsx).
                - Información Importante: Son datos referenciales
                - Hora de Actualización: 8:00 a.m.
                ''')

if selected == 'Busqueda de Personas':
    st.title('Búsqueda de Personas')

    st.header('Filtrar por atributos')
    with st.expander('Filtrar Desaparecidos'):
        col1, col2, col3 = st.columns(3)

        pais = col1.selectbox('Selecciona un País de Nacimiento:', ['Todos'] + sorted(df['pais_nacimiento'].unique().tolist()))
        edad = col2.selectbox('Selecciona una Edad:', ['Todos'] + sorted(df['edad'].unique().tolist()))
        dependencia = col3.selectbox('Selecciona una Dependencia Policial:', ['Todos'] + sorted(df['dependencia_policial'].unique().tolist()))

        filtered_df = df.copy()
        if pais != 'Todos':
            filtered_df = filtered_df[filtered_df['pais_nacimiento'] == pais]
        if edad != 'Todos':
            filtered_df = filtered_df[filtered_df['edad'] == edad]
        if dependencia != 'Todos':
            filtered_df = filtered_df[filtered_df['dependencia_policial'] == dependencia]

        st.write(f"Resultados Filtrados: {len(filtered_df)}")
        st.dataframe(filtered_df)

        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df_to_csv(filtered_df)
        st.download_button(
            label="Exportar Resultados Filtrados a CSV",
            data=csv,
            file_name='resultados_filtrados.csv',
            mime='text/csv',
        )

    st.header('Buscar por Nombre')
    with st.expander('Buscar Desaparecidos por Nombre'):
        search_name = st.text_input('Ingresa el nombre a buscar:')

        if search_name:
            search_results = df[df['nombres'].str.contains(search_name, case=False, na=False)]
            if not search_results.empty:
                st.write(f"Resultados de búsqueda: {len(search_results)}")
                for index, row in search_results.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"### {row['nombres']}")
                        st.write(f"**Edad:** {row['edad']}")
                        st.write(f"**País de Nacimiento:** {row['pais_nacimiento']}")
                        st.write(f"**Dependencia Policial:** {row['dependencia_policial']}")
                        st.write(f"**Lugar del Hecho:** {row['lugar_hecho']}")
                        st.write(f"**Fecha de Denuncia:** {row['fecha_denuncia']}")
                        st.write(f"**Fecha del Hecho:** {row['fecha_hecho']}")
                        st.write(f"**Circunstancias:** {row['circunstancias']}")
                        st.write(f"**Aparecido:** {'Sí' if row['aparecido'] else 'No'}")
                        st.write(f"**Fecha de Aparición:** {row['fecha_aparicion'] if pd.notna(row['fecha_aparicion']) else 'N/A'}")
                        st.write(f"**Hora de Aparición:** {row['hora_aparicion'] if pd.notna(row['hora_aparicion']) else 'N/A'}")
                    with col2:
                        if pd.notna(row['url']):
                            st.image(row['url'], caption=row['nombres'], use_column_width=True)
            else:
                st.warning('No se encontraron resultados para el nombre ingresado.')

if selected == "Dashboard":
    total_appeared = df['aparecidos'].sum()
    total_disappeared = len(df) - df['aparecidos'].sum()
    percentage_appeared = (total_appeared / total_disappeared) * 100 if total_disappeared != 0 else 0
    region_most_disappeared = df['region'].value_counts().idxmax()

    st.title('Dashboard de Personas Desaparecidas')
    
    # Use containers for better layout control
    header_container = st.container()
    metrics_container = st.container()
    charts_container = st.container()

    with header_container:
        st.markdown("<hr style='border: 1px solid #FF6F61;'>", unsafe_allow_html=True)

    with metrics_container:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Cantidad de Desaparecidos", value=total_disappeared)
        with col2:
            st.metric(label="Cantidad de Aparecidos", value=total_appeared)
        with col3:
            st.metric(label="Región con más Desaparecidos", value=region_most_disappeared)

    with charts_container:
        st.markdown("<h2 style='color: #FF6F61;'>Visualizaciones</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid #FF6F61;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            fig_age = px.histogram(df, x='edad', nbins=20, title='Distribución de Edad', color_discrete_sequence=['#00CC96'])
            age_counts = df['edad'].value_counts().reset_index()
            age_counts.columns = ['Edad', 'Count']
            max_age = age_counts.iloc[age_counts['Count'].idxmax()]['Edad']
            max_count = age_counts['Count'].max()
            min_age = age_counts.iloc[age_counts['Count'].idxmin()]['Edad']
            min_count = age_counts['Count'].min()
            mean_count = age_counts['Count'].mean()

            fig_age.add_annotation(x=max_age, y=max_count,
                                   text=f'Edad: {max_age}<br>Max: {max_count}',
                                   showarrow=True, arrowhead=1, ax=0, ay=-40)
            fig_age.add_annotation(x=min_age, y=min_count,
                                   text=f'Edad: {min_age}<br>Min: {min_count}',
                                   showarrow=True, arrowhead=1, ax=0, ay=40)
            fig_age.add_shape(type='line', x0=df['edad'].min(), x1=df['edad'].max(), y0=mean_count, y1=mean_count,
                              line=dict(color='RoyalBlue', dash='dash'))
            fig_age.add_annotation(x=df['edad'].max(), y=mean_count,
                                   text=f'Mean: {mean_count:.2f}', showarrow=False, yshift=10)
            #fig_age.update_traces(marker_color='#00CC96', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
            #fig_age.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#FFFFFF', title_font_color='#FF6F61', title_font_size=20)
            st.plotly_chart(fig_age)

        with col2:
            st.subheader('Número de Personas Desaparecidas por País de Nacimiento')
            country_counts = df['pais_nacimiento'].value_counts().reset_index()
            country_counts.columns = ['País de Nacimiento', 'Número de Personas']
            fig_country = px.pie(country_counts, names='País de Nacimiento', values='Número de Personas',
                                 title='Número de Personas Desaparecidas por País de Nacimiento',
                                 color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4)
            fig_country.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_country)

        with col1:
            st.subheader('Personas Desaparecidas por Dependencia Policial')
            top_n = st.slider('Selecciona el número de dependencias policiales a mostrar:', min_value=1, max_value=20, value=10)
            police_counts = df['dependencia_policial'].value_counts().reset_index()
            police_counts.columns = ['Dependencia Policial', 'Número de Personas']
            top_police_counts = police_counts.head(top_n)
            fig_police = px.bar(top_police_counts, x='Dependencia Policial', y='Número de Personas',
                                title=f'Top {top_n} Dependencias Policiales con más Personas Desaparecidas',
                                color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig_police)

        with col2:
            st.subheader('Personas Desaparecidas a lo Largo del Tiempo')
            df['fecha_denuncia'] = pd.to_datetime(df['fecha_denuncia'], format='%d/%m/%Y', errors='coerce')
            df_time = df['fecha_denuncia'].value_counts().sort_index().reset_index()
            df_time.columns = ['Fecha de Denuncia', 'Número de Personas']
            fig_time = px.line(df_time, x='Fecha de Denuncia', y='Número de Personas', title='Personas Desaparecidas a lo Largo del Tiempo', color_discrete_sequence=['#AB63FA'])
            st.plotly_chart(fig_time)
            
    st.header('Desapariciones por Horas y Días')

    # Supongamos que tu DataFrame se llama df y ya tiene las columnas 'fecha_hecho' y 'hora_hecho'
    # Convierte las columnas 'fecha_hecho' y 'hora_hecho' a formato datetime
    df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'], format='%d/%m/%Y')
    df['hora_hecho'] = pd.to_datetime(df['hora_hecho'], format='%H:%M:%S').dt.time

    # Combina 'fecha_hecho' y 'hora_hecho' en una sola columna datetime
    df['datetime_hecho'] = df.apply(lambda row: pd.to_datetime(f"{row['fecha_hecho'].date()} {row['hora_hecho']}"), axis=1)

    # Extrae el día de la semana y la hora
    df['day_of_week'] = df['fecha_hecho'].dt.day_name()
    df['hour'] = df['datetime_hecho'].dt.hour


    min_date = df['fecha_hecho'].min()
    max_date = df['fecha_hecho'].max()

    selected_week = st.date_input("Selecciona una semana", [min_date, min_date + pd.Timedelta(days=6)])
    start_date, end_date = selected_week[0], selected_week[1]

    # Convertir start_date y end_date a datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[(df['fecha_hecho'] >= start_date) & (df['fecha_hecho'] <= end_date)]

    # Pivot table para el heatmap
    heatmap_data = filtered_df.pivot_table(index='day_of_week', columns='hour', aggfunc='size', fill_value=0)

    # Ordenar los días de la semana
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(ordered_days)

    fig_heatmap = px.imshow(heatmap_data,
                            labels=dict(x="Hora", y="Día de la Semana", color="Número de Desaparecidos"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale='Viridis',
                            title=f'Desapariciones del {start_date.strftime("%d/%m/%Y")} al {end_date.strftime("%d/%m/%Y")}')
    fig_heatmap.update_layout(
        autosize=False,
        width=1200,  # Ajusta el ancho
        height=600,  # Ajusta la altura
        margin=dict(l=50, r=50, b=50, t=50, pad=4)
    )


    st.plotly_chart(fig_heatmap)

    # Footer
    st.markdown("<hr style='border: 1px solid #FF6F61;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #FF6F61;'>© 2024 Los Saqueadores</h4>", unsafe_allow_html=True)


if selected == "Apriori":
    st.header('Patrones frecuentes y reglas de asociación')
    file_path = 'Resultados_apriori.xlsx'
    excel_data = pd.ExcelFile(file_path)

    # Mostrar las hojas del archivo Excel
    sheet_names = excel_data.sheet_names
    selected_sheet = st.selectbox('Selecciona una hoja', sheet_names)

    # Cargar la hoja seleccionada
    df = pd.read_excel(file_path, sheet_name=selected_sheet)

    # Mostrar la tabla de manera estética
    col1, col2 = st.columns([4, 3])

    # Mostrar la tabla en la primera columna
    with col1:
        st.header(f'Apriori: {selected_sheet}')
        st.dataframe(df)

    # Mostrar la imagen en la segunda columna
    with col2:
        st.markdown("<h4 style='text-align: center;'>Apriori Algorithm</h2>", unsafe_allow_html=True)
        st.image('images/apriori.png', caption='Apriori Algorithm', use_column_width=True)



if selected == "Random Forest":
    st.header('Random Forest')


if selected == "Clusters":
    st.header('Grupos Asociados')
    cluster_data = {
        "Cluster_0_vs_Cluster_1": [-0.002641, 0.190385, 3.573445, 0.046478, 0.025184, -0.139584, -0.034321, 0.004827, 0.036518, -0.093174],
        "Cluster_1_vs_Cluster_0": [0.002801, -0.182160, -3.359249, -0.047260, -0.025308, 0.149832, 0.034357, -0.004926, -0.036908, 0.102972]
    }
    cluster_index = ["Horas para Denunciar", "LUGAR DEL HECHO", "Instructor Policial", "EDAD", "ESTATURA", "NARIZ", "TEZ", "SANGRE", "CONTEXTURA", "FENOTIPO"]
    cluster_df = pd.DataFrame(cluster_data, index=cluster_index)
    
    col1, col2 = st.columns([4, 3])

    # Mostrar la tabla en la primera columna
    with col1:
        # Mostrar la nueva tabla
        st.header('Comparación de Clústeres')
        st.dataframe(cluster_df, use_container_width=True)

    # Mostrar la imagen en la segunda columna
    with col2:
        st.markdown("<h4 style='text-align: center;'>TSNE</h2>", unsafe_allow_html=True)
        st.image('images/tnse.jpeg', caption='', use_column_width=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        st.header('Perfiles')
        st.image('images/perfiles.png', caption='')
        
if selected == "ARIMA":
    st.header('Modelo Estacional de Tendencias')
    col1, col2 = st.columns([5, 1])
    with col1:
        st.image('images/arima.jpeg', caption='', use_column_width=True)