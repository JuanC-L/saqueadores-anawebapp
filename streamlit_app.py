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
warnings.filterwarnings('ignore')

# Crea la cadena de conexión sin usuario y contraseña (usando la autenticación de Windows)




# Load the Excel file into a DataFrame
file_path = "Scrapeadores.xlsx"
df = pd.read_excel(file_path)

# ##### inicio de sesión
# def creds_entered():
#     if st.session_state["user"].strip() == "admin" and st.session_state["passwd"].strip() == "admin":
#         st.session_state["authenticated"] = True
#     else:
#         st.session_state["authenticated"] = False 
#         if not st.session_state["passwd"]:
#             st.warning("Please enter password.") 
#         elif not st.session_state["user"]:
#             st.warning("Please enter username.")
#         else:
#             st.error("Invalid Username/Password :face_with_raised_eyebrow:")

# def authenticate_user():
#     if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
#         st.text_input(label="username", key="user", on_change=creds_entered)
#         st.text_input(label="password", key="passwd", type="password", on_change=creds_entered)
#         return False
#     else:
#         return True
        
#### el usuario ingreso los datos correctos
#if authenticate_user():

# Mostrar el gráfico en la aplicación Streamlit

## configuración del side bar

# Configuration of the side bar
st.set_page_config(
    page_title="Los Saqueadores",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
alt.themes.enable("dark")


# Use Google Fonts for a pleasant font
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

st.sidebar.markdown("<h1 class='sidebar-title' style='postion:center;'>Los Saqueadores</h1>", unsafe_allow_html=True)

with st.sidebar:
    # Horizontal menu
    selected = option_menu(
        menu_title=None,
        options=["Home", "Busqueda de Personas","Dashboards 1", "Dashboards 2", "Dashboards 3"],
        icons=["house","person-fill", "coin", "book", "person-fill"],
        menu_icon="cast",
        default_index=0,
        # orientation="horizontal",
    )

if selected == "Home":
    st.markdown("<h1 class='header'>Centro de Información de Personas Desaparecidas</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    # Embed the preview of the website
    with col1:
        st.markdown("""
            <div class="embed-container">
                <iframe src="https://desaparecidosenperu.policia.gob.pe" frameborder="0" allowfullscreen></iframe>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Add additional content as shown in the image
        st.markdown("<div class='content' style='font-size: 18px; padding-bottom: 30px;'>Proyecto que busca dar visibilidad y trazabilidad a las personas desaparecidas en Perú. Se hace uso de datos del RENIPED actualizados diariamente para un análisis y predicción de estos.</div>", unsafe_allow_html=True)

        st.image("images\desap.png", use_column_width=True)
        with st.expander('About', expanded=True):
            st.write('''
                - Datos: [Historico 2024](https://desaparecidosenperu.policia.gob.pe/WebDesaparecidos/documento/2024.xlsx).
                - Información Importante: No se
                - Hora de Actualización: 8:00 a.m.
                ''')
        

# Your existing content here
if selected=='Busqueda de Personas':


    # Streamlit UI
    st.title('Búsqueda de Personas')

    # Filter Section
    st.header('Filtrar por atributos')
    with st.expander('Filtrar Desaparecidos'):
        col1, col2, col3 = st.columns(3)

        # Filtrar por PAIS DE NACIMIENTO
        pais = col1.selectbox('Selecciona un País de Nacimiento:', ['Todos'] + sorted(df['PAIS DE NACIMIENTO'].unique().tolist()))

        # Filtrar por EDAD
        edad = col2.selectbox('Selecciona una Edad:', ['Todos'] + sorted(df['EDAD'].unique().tolist()))

        # Filtrar por Dependencia Policial
        dependencia = col3.selectbox('Selecciona una Dependencia Policial:', ['Todos'] + sorted(df['Dependencia Policial'].unique().tolist()))

        # Apply filters
        filtered_df = df.copy()
        if pais != 'Todos':
            filtered_df = filtered_df[filtered_df['PAIS DE NACIMIENTO'] == pais]
        if edad != 'Todos':
            filtered_df = filtered_df[filtered_df['EDAD'] == edad]
        if dependencia != 'Todos':
            filtered_df = filtered_df[filtered_df['Dependencia Policial'] == dependencia]

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

    # Search Section
    st.header('Buscar por Nombre')
    with st.expander('Buscar Desaparecidos por Nombre'):
        search_name = st.text_input('Ingresa el nombre a buscar:')

        if search_name:
            search_results = df[df['NOMBRES'].str.contains(search_name, case=False, na=False)]
            if not search_results.empty:
                st.write(f"Resultados de búsqueda: {len(search_results)}")
                for index, row in search_results.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"### {row['NOMBRES']}")
                        st.write(f"**Edad:** {row['EDAD']}")
                        st.write(f"**País de Nacimiento:** {row['PAIS DE NACIMIENTO']}")
                        st.write(f"**Dependencia Policial:** {row['Dependencia Policial']}")
                        st.write(f"**Lugar del Hecho:** {row['LUGAR DEL HECHO']}")
                        st.write(f"**Fecha de Denuncia:** {row['Fecha de Denuncia']}")
                        st.write(f"**Fecha del Hecho:** {row['Fecha del Hecho']}")
                        st.write(f"**Aparecido:** {'Sí' if row['Aparecido'] else 'No'}")
                        st.write(f"**Fecha de Aparición:** {row['Fecha de Aparición'] if True else 'N/A'}")
                        st.write(f"**Hora de Aparición:** {row['Hora de Aparición'] if True else 'N/A'}")
                    with col2:
                        if pd.notna(row['img']):
                            st.image(row['img'], caption=row['NOMBRES'], use_column_width=True)
            else:
                st.warning('No se encontraron resultados para el nombre ingresado.')



if selected=="Dashboards 1":
    st.title('Dashboard de Personas Desaparecidas')
    
### segundo dashboard: LIBROS
if selected=="Dashboards 2":



    # Ensure 'Fecha de Denuncia' is in datetime format
    df['Fecha de Denuncia'] = pd.to_datetime(df['Fecha de Denuncia'], errors='coerce')
    def convert_time_format(time_str):
        if pd.isna(time_str):
            return None
        try:
            return pd.to_datetime(time_str, format='%I:%M:%S %p').time()  # Handle "a.m." and "p.m."
        except ValueError:
            try:
                return pd.to_datetime(time_str, format='%H:%M:%S').time()  # Handle 24-hour format
            except ValueError:
                return None

    df['Hora de Denuncia'] = df['Hora de Denuncia'].apply(convert_time_format)

    # Calculate metrics
    total_disappeared = len(df)
    total_appeared = df['Aparecido'].sum()
    percentage_appeared = (total_appeared / total_disappeared) * 100
    region_most_disappeared = df['PAIS DE NACIMIENTO'].value_counts().idxmax()

    # Extract month and hour from 'Fecha de Denuncia'
    df['Month'] = df['Fecha de Denuncia'].dt.month
    df['Hour'] = df['Fecha de Denuncia'].dt.hour
    df['Day'] = df['Fecha de Denuncia'].dt.day_name()

    # Streamlit UI
    st.title('Dashboard de Personas Desaparecidas')

    # Interactive filtering for top police departments
    top_n = st.slider('Selecciona el número de dependencias policiales a mostrar:', min_value=1, max_value=20, value=10)


    # Create two columns with spacing for the plots
    col1, space1, col2 = st.columns([4, 1, 4])

    # Plot 1: Distribution of Age
    with col1:
        st.subheader('Distribución de Edad')
        fig_age = px.histogram(df, x='EDAD', nbins=20, title='Distribución de Edad', color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig_age)

    # Plot 2: Number of Missing Persons by Country of Birth
    with col2:
        st.subheader('Número de Personas Desaparecidas por País de Nacimiento')
        country_counts = df['PAIS DE NACIMIENTO'].value_counts().reset_index()
        country_counts.columns = ['País de Nacimiento', 'Número de Personas']
        fig_country = px.pie(country_counts, names='País de Nacimiento', values='Número de Personas', 
                            title='Número de Personas Desaparecidas por País de Nacimiento', 
                            color_discrete_sequence=px.colors.qualitative.Pastel,
                            hole=0.4)
        fig_country.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_country)

    # Create a new row of columns with spacing for the next plots
    col3, space2, col4 = st.columns([4, 1, 4])

    # Plot 4: Missing Persons Over Time
    with col3:
        st.subheader('Personas Desaparecidas a lo Largo del Tiempo')
        df_time = df['Fecha de Denuncia'].dt.to_period('M').value_counts().sort_index().reset_index()
        df_time.columns = ['Fecha de Denuncia', 'Número de Personas']
        df_time['Fecha de Denuncia'] = df_time['Fecha de Denuncia'].astype(str)  # Convert Period to string
        fig_time = px.line(df_time, x='Fecha de Denuncia', y='Número de Personas', title='Personas Desaparecidas a lo Largo del Tiempo', color_discrete_sequence=['#AB63FA'])
        st.plotly_chart(fig_time)

    # Heatmap for disappearances by hour and day
    st.header('Desapariciones por Horas y Días')
    selected_month = st.selectbox('Selecciona un Mes:', sorted(df['Month'].dropna().unique().tolist()))

    filtered_df = df[df['Month'] == selected_month]

    heatmap_data = filtered_df.pivot_table(index='Day', columns='Hour', aggfunc='size', fill_value=0)

    fig_heatmap = px.imshow(heatmap_data, 
                            labels=dict(x="Hora", y="Día de la Semana", color="Número de Desaparecidos"),
                            x=heatmap_data.columns, 
                            y=heatmap_data.index,
                            color_continuous_scale='Viridis',
                            title=f'Desapariciones en el Mes {selected_month}')

    st.plotly_chart(fig_heatmap)



 



    # ### sidebar part
    # st.sidebar.subheader('Conteo de Idiomas')
    # prueba = st.sidebar.selectbox('Dispoible o no disponible', ('Disp', 'NoDisp'))

    # st.sidebar.subheader('Top Propietarios')
    # plot_nums = st.sidebar.slider('Numero del top', 1, 20, 5)

    
    # st.sidebar.subheader('WordCloud')
    # words = st.sidebar.slider('Cantidad de palabras', 10, 80, 40)

    # st.sidebar.markdown('''
    # ---
    # Opus Hub).
    # ''')

    # ### parte dentro de la página
    # st.markdown('### Métricas de Libros')
    # col1, col2 = st.columns(2)

    # ### Categoría con más libros
    # querymetr1 = "select top 1 categoria.descripcion,count(*) as 'Total' from clasifica inner join categoria on clasifica.codCat=categoria.codCat group by clasifica.codCat,categoria.descripcion order by Total desc"
    # dfm1 = pd.read_sql_query(querymetr1, conn)
    # col1.metric("Categoría con más libros", str(list(dfm1['descripcion'])[0]), str(list(dfm1['Total'])[0]))

    # ### cantidad de libros con rating máximo
    # querymetr4 = "select MAX(rating) as Maximo from detalle_Web inner join libro on libro.codWeb = detalle_Web.codWeb"
    # dfm4 = pd.read_sql_query(querymetr4, conn)
    # querymetr5 = "select count(*) as Total from detalle_Web inner join libro on libro.codWeb = detalle_Web.codWeb where rating = (select MAX(rating) from detalle_Web inner join libro on libro.codWeb = detalle_Web.codWeb)"
    # dfm5 = pd.read_sql_query(querymetr5, conn)
    # col2.metric("Rating máximo por los usuarios",  str(list(dfm4['Maximo'])[0]),str(list(dfm5['Total'])[0])+' libros')

    # c1, c2 = st.columns((4,6))

    # with c1:

    #     ### Conteo de libros según idioma
    #     query = "select * from libro "

    #     # Ejecutar la consulta y cargar los resultados en un DataFrame de Pandas
    #     df = pd.read_sql_query(query, conn)
    #     df=df[['disponibilidad','idioma']]
    #     df['Disp'] = df.apply(lambda row: row['idioma'] if row['disponibilidad']==True else None, axis=1)
    #     df['NoDisp'] = df.apply(lambda row: row['idioma'] if row['disponibilidad']==False else None, axis=1)

    #     idioma_counts = df[prueba].value_counts().reset_index()
    #     idioma_counts.columns = [prueba, 'Cantidad']

    #     # Crear un gráfico de barras interactivo con Plotly
    #     fig = px.bar(idioma_counts, x=prueba, y='Cantidad', title='Conteo de Idiomas')
    #     fig.update_layout(xaxis_title='Idioma', yaxis_title='Cantidad')
    #     st.plotly_chart(fig, use_container_width=True)

    # with c2:
    #     query2 = "SELECT * FROM propietario"
    #     df2 = pd.read_sql_query(query2, conn)

    #     # Seleccionar las top 10 filas
    #     df_top10 = df2.sort_values(by='cantidad_libros', ascending=False).head(plot_nums)

    #     # Crear el gráfico de barras con Plotly Express
    #     fig2 = px.bar(df_top10, x='pseudonimo', y='cantidad_libros', title='Top de Propietarios con más Libros',
    #                 labels={'cantidad_libros': 'Cantidad de Libros'},
    #                 color='cantidad_libros', # Colorear barras según la cantidad de libros
    #                 color_continuous_scale='Viridis', # Escala de color
    #                 )

    #     # Personalizar el diseño del gráfico
    #     fig2.update_layout(
    #         xaxis_title='Propietario',
    #         yaxis_title='Cantidad de Libros',
    #         title_text='Top de Propietarios con más Libros',
    #         title_x=0.5,  # Centrar el título
    #         plot_bgcolor='rgba(0,0,0,0)',  # Fondo del gráfico transparente
    #     )

    #     # Añadir etiquetas a las barras
    #     fig2.update_traces(texttemplate='%{y}', textposition='outside')
    #     st.plotly_chart(fig2, use_container_width=True)


    # c3, c4 = st.columns((6,4))

    # with c3:
    #     st.markdown('### WORD CLOUD')

    #     #### WORD CLOUD
    #     # Función para filtrar adjetivos
    #     def filter_adjectives(text):
    #         words = word_tokenize(text)
    #         tagged_words = pos_tag(words)
    #         adjectives = [word.lower() for word, pos in tagged_words if pos.startswith('JJ') and word.isalnum()]
    #         return ' '.join(adjectives)

    #     # Obtener datos desde la base de datos (sustituye esto con tu propia lógica de obtención de datos)
    #     # Esto es solo un ejemplo para ilustrar el código con Streamlit
    #     querycl = "select resenha from obtiene where rating=10"
    #     dfcl = pd.read_sql_query(querycl, conn)
    #     dfcl = dfcl.dropna()

    #     # Agregar palabras personalizadas a la lista de stopwords
    #     custom_stopwords = set(['example', 'significant', 'books', 'one'])  # Agrega las palabras que desees
    #     stop_words = set(stopwords.words('english') + list(STOPWORDS) + list(custom_stopwords))

    #     # Filtrar adjetivos en todas las reseñas
    #     dfcl['adjectives'] = dfcl['resenha'].apply(filter_adjectives)

    #     # Concatenar todas los adjetivos en un solo texto
    #     text = ' '.join(dfcl['adjectives'])

    #     # Crear el WordCloud
    #     wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=words).generate(text)

    #     # Configuración de la interfaz de Streamlit
    #     st.title('WordCloud de Adjetivos en Reseñas')
    #     # Mostrar el WordCloud utilizando Streamlit
    #     st.image(wordcloud.to_array())
    



### tercer dashboard
if selected=="Dashboards 3":
    # Streamlit UI
    total_disappeared = len(df)
    total_appeared = df['Aparecido'].sum()
    percentage_appeared = (total_appeared / total_disappeared) * 100
    region_most_disappeared = df['PAIS DE NACIMIENTO'].value_counts().idxmax()

    # Streamlit UI
    st.title('Dashboard de Personas Desaparecidas')
    # Display metrics
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric(label="Cantidad de Desaparecidos", value=total_disappeared)

    with col2:
        st.metric(label="Cantidad de Aparecidos", value=total_appeared)
        # st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        # # Circular progress bar
        # fig = go.Figure(go.Indicator(
        #     mode="gauge+number",
        #     value=percentage_appeared,
        #     title={'text': "Aparecidos (%)"},
        #     gauge={
        #         'axis': {'range': [0, 100]},
        #         'bar': {'color': "green"},
        #         'bgcolor': "white",
        #         'steps': [
        #             {'range': [0, percentage_appeared], 'color': "lightgreen"},
        #             {'range': [percentage_appeared, 100], 'color': "lightgray"}
        #         ],
        #         'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': percentage_appeared}
        #     }
        # ))
        # fig.update_layout(width=200, height=200, margin=dict(t=0, b=0, l=0, r=0))
        # st.plotly_chart(fig, use_container_width=True)
        # st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.metric(label="Región con más Desaparecidos", value=region_most_disappeared)

        # Create two columns for the plots
    col1, col2 = st.columns([0.8,0.8],gap="large")

    # Plot 1: Distribution of Age
    with col1:

        st.subheader('Distribución de Edad')
        fig_age = px.histogram(df, x='EDAD', nbins=20, title='Distribución de Edad', color_discrete_sequence=['#A1D725'])

        # Calculate statistics
        age_counts = df['EDAD'].value_counts().reset_index()
        age_counts.columns = ['Edad', 'Count']
        max_count = age_counts['Count'].max()
        min_count = age_counts['Count'].min()
        mean_count = age_counts['Count'].mean()

        # Add annotations for max and min values
        fig_age.add_annotation(x=age_counts['Edad'][age_counts['Count'].idxmax()],
                            y=max_count, text=f'Max: {max_count}', showarrow=True, arrowhead=1, ax=0, ay=-40)
        fig_age.add_annotation(x=age_counts['Edad'][age_counts['Count'].idxmin()],
                            y=min_count, text=f'Min: {min_count}', showarrow=True, arrowhead=1, ax=0, ay=40)

        # Add a line for the mean value
        fig_age.add_shape(type='line', x0=df['EDAD'].min(), x1=df['EDAD'].max(), y0=mean_count, y1=mean_count,
                        line=dict(color='RoyalBlue', dash='dash'))
        fig_age.add_annotation(x=df['EDAD'].max(), y=mean_count, 
                            text=f'Mean: {mean_count:.2f}', showarrow=False, yshift=10)

        # Show the plot
        st.plotly_chart(fig_age)

    # Plot 2: Number of Missing Persons by Country of Birth
    with col2:
        st.subheader('Número de Personas Desaparecidas por País de Nacimiento')
        country_counts = df['PAIS DE NACIMIENTO'].value_counts().reset_index()
        country_counts.columns = ['País de Nacimiento', 'Número de Personas']
        fig_country = px.pie(country_counts, names='País de Nacimiento', values='Número de Personas', 
                            title='Número de Personas Desaparecidas por País de Nacimiento', 
                            color_discrete_sequence=px.colors.qualitative.Pastel,
                            hole=0.4)
        fig_country.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_country)

    # Plot 3: Missing Persons by Police Department
# Interactive filtering for top police departments


    with col1:
        st.subheader('Personas Desaparecidas por Dependencia Policial')
        top_n = st.slider('Selecciona el número de dependencias policiales a mostrar:', min_value=1, max_value=20, value=10)
        police_counts = df['Dependencia Policial'].value_counts().reset_index()
        police_counts.columns = ['Dependencia Policial', 'Número de Personas']
        top_police_counts = police_counts.head(top_n)
        fig_police = px.bar(top_police_counts, x='Dependencia Policial', y='Número de Personas',
                            title=f'Top {top_n} Dependencias Policiales con más Personas Desaparecidas',
                            color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig_police)

    # Plot 4: Missing Persons Over Time
    with col2:
        st.subheader('Personas Desaparecidas a lo Largo del Tiempo')
        df['Fecha de Denuncia'] = pd.to_datetime(df['Fecha de Denuncia'], errors='coerce')
        df_time = df['Fecha de Denuncia'].dt.to_period('M').value_counts().sort_index().reset_index()
        df_time.columns = ['Fecha de Denuncia', 'Número de Personas']
        df_time['Fecha de Denuncia'] = df_time['Fecha de Denuncia'].astype(str)  # Convert Period to string
        fig_time = px.line(df_time, x='Fecha de Denuncia', y='Número de Personas', title='Personas Desaparecidas a lo Largo del Tiempo', color_discrete_sequence=['#AB63FA'])
        st.plotly_chart(fig_time)
























    # ### contenido del sidebar
    # st.sidebar.subheader('Rango de top')
    # # Añadir un slider para seleccionar el rango (1-30)
    # selected_range = st.sidebar.slider("Seleccionar Rango", 1, 30, value=(1, 10))

    # st.sidebar.markdown('''
    # ---
    # Opus Hub).
    # ''')

    # ### contenido dentro de la página
    # st.markdown('### Métricas de Usuarios')

    # col1, col2, col3 = st.columns(3)
    # ### Total de vetos de todos los usuarios
    # querymetr3 = "select count(*) as 'Total' from obtiene where veto=1"
    # dfm3 = pd.read_sql_query(querymetr3, conn)
    # col1.metric("Usuarios vetados en transacción", 'Vetos totales', str(list(dfm3['Total']*-1)[0]))
    
    # c1, c2 = st.columns((3,7))
    # with c1:
    #     ### grafico donnut chart por rango etario
    #     queryedad= """SELECT AgeRange, count(*) as 'Total'
    #     FROM (
    #         SELECT
    #             CASE 
    #                 WHEN DATEDIFF(day, fechanac, GETDATE()) < 18 * 365 THEN 'Menor de 18'
    #                 WHEN DATEDIFF(day, fechanac, GETDATE()) BETWEEN 18 * 365 AND 27 * 365 THEN 'edades 18-26'
    #                 WHEN DATEDIFF(day, fechanac, GETDATE()) BETWEEN 27 * 365 AND 60 * 365 THEN 'edades 27-59'
    #                 WHEN DATEDIFF(day, fechanac, GETDATE()) >= 60 * 365 THEN 'Mayores de 60'
    #             END as AgeRange,
    #             1 as TotalOrders
    #         FROM
    #             detallecuenta
    #     ) AS SourceTable
    #     GROUP BY AgeRange;"""

    #     dfedad = pd.read_sql_query(queryedad, conn)

    #     # Crear el gráfico donut con Plotly Express
    #     figedad = px.pie(dfedad, names='AgeRange', values='Total', hole=0.3)

    #     # Añadir etiquetas y porcentajes
    #     figedad.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1], textposition='inside')

    #     # Personalizar el diseño del gráfico
    #     figedad.update_layout(
    #         title='Rangos etarios en porcentaje',
    #         showlegend=False,  # Ocultar leyenda, ya que las etiquetas están dentro del gráfico
    #     )

    #     # Mostrar el gráfico
    #     st.plotly_chart(figedad, use_container_width=True)

    # with c2:
    #     ##### grafico de cantidad de ordenes por rango etario
    #     querycant_por_edad = """SELECT AgeRange, SUM(TotalOrders) as 'Cantidad' 
    #             FROM (
    #                 SELECT 
    #                     CASE 
    #                         WHEN DATEDIFF(day, fechanac, GETDATE()) < 18 * 365 THEN 'Menor de 18'
    #                         WHEN DATEDIFF(day, fechanac, GETDATE()) BETWEEN 18 * 365 AND 27 * 365 THEN 'edades 18-26'
    #                         WHEN DATEDIFF(day, fechanac, GETDATE()) BETWEEN 27 * 365 AND 60 * 365 THEN 'edades 27-59'
    #                         WHEN DATEDIFF(day, fechanac, GETDATE()) >= 60 * 365 THEN 'Mayores de 60'
    #                     END as AgeRange,
    #                     1 as TotalOrders
    #                 FROM
    #                     detallecuenta
    #                     INNER JOIN cuenta ON detallecuenta.HashUs = cuenta.HashUS
    #                     INNER JOIN orden_venta ON orden_venta.HashUs = cuenta.HashUS
    #             ) AS SourceTable
    #             GROUP BY AgeRange;"""

    #     # Leer los resultados de la consulta en un DataFrame de pandas
    #     dfcant_por_edad = pd.read_sql_query(querycant_por_edad, conn)

    #     # Definir el orden de las categorías en el eje x
    #     orden_categorias = ['Menor de 18', 'edades 18-26', 'edades 27-59', 'Mayores de 60']

    #     # Crear un gráfico de barras interactivo con Plotly
    #     figcant = px.bar(
    #         dfcant_por_edad,
    #         x='AgeRange',
    #         y='Cantidad',
    #         title='Conteo de Ordenes por Rango Etario',
    #         labels={'Catidad': 'Número de Órdenes'},
    #         color='AgeRange',
    #         category_orders={'AgeRange': orden_categorias},  # Especificar el orden de las categorías
    #     )

    #     # Personalizar el diseño del gráfico
    #     figcant.update_layout(
    #         xaxis_title='Rango Etario',
    #         yaxis_title='Número de Órdenes',
    #         legend_title='Grupo de Edad',
    #         barmode='stack',  # Puedes cambiarlo a 'group' si prefieres barras agrupadas
    #     )

    #     # Mostrar el gráfico en Streamlit
    #     st.plotly_chart(figcant)

    # c3, c4 = st.columns((7,3))
    # with c3:
    #     ### grafico de usuarios más activos segun su ultima fecha de uso
    #     # Consulta SQL para obtener nombres y apellidos de los usuarios más activos
    #     querytop = "SELECT Nombre, Apellido FROM vincula INNER JOIN cuenta ON vincula.HashUs = cuenta.HashUS INNER JOIN detallecuenta ON detallecuenta.HashUs = cuenta.HashUS ORDER BY ultimo_uso ASC"

    #     # Cargar datos en un DataFrame de pandas
    #     dftopuser = pd.read_sql(querytop, conn)

    #     # Agregar una columna de ranking ascendente
    #     dftopuser['Ranking'] = range(1, len(dftopuser) + 1)


    #     # Filtrar el DataFrame según el rango seleccionado y ordenar por ranking ascendente
    #     filtered_df = dftopuser.iloc[selected_range[0] - 1:selected_range[1]]


    #     # Establecer altura de fila fija
    #     altura_fila = 40

    #     # Crear una tabla con Plotly y personalizar la apariencia
    #     fig = go.Figure(data=[go.Table(
    #         header=dict(values=['Ranking', 'Nombre', 'Apellido'],
    #                     fill_color='#1f77b4',  # Color de fondo del encabezado
    #                     font=dict(color='white', size=14),  # Color y tamaño del texto del encabezado
    #                     align='center',
    #                     line_color='black',  # Color de las líneas del encabezado
    #                     height=altura_fila,  # Altura fija del encabezado
    #                     ),
    #         cells=dict(values=[filtered_df.Ranking, filtered_df.Nombre, filtered_df.Apellido],
    #                 fill_color='#EDF0F6',  # Color de fondo de las celdas
    #                 font=dict(color='black', size=12),  # Color y tamaño del texto de las celdas
    #                 align='center',
    #                 line_color='black',  # Color de las líneas de las celdas
    #                 height=altura_fila,  # Altura fija de las celdas
    #                 )
    #     )])

    #     # Estilo de la figura
    #     fig.update_layout(
    #         title='Top Usuarios con Ranking',
    #     )

    #     # Mostrar la tabla
    #     st.plotly_chart(fig)
    # with c4:
    #     querydonut = "select tipo from dispositivos"
    #     dfdonut = pd.read_sql_query(querydonut, conn)

    #     # Crear el gráfico donut con Plotly Express
    #     fig = px.pie(dfdonut, names='tipo', hole=0.3)

    #     # Añadir etiquetas y porcentajes
    #     fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1], textposition='inside')

    #     # Personalizar el diseño del gráfico
    #     fig.update_layout(
    #         title='Dispositivos en porcentaje',
    #         showlegend=False,  # Ocultar leyenda, ya que las etiquetas están dentro del gráfico
    #     )

    #     # Mostrar el gráfico
    #     st.plotly_chart(fig, use_container_width=True)

        

