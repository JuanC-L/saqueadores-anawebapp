
# Streamlit como gestor de Opus Hub

Esta aplicación de Streamlit permite interactuar con la base de datos de Opus Hub para consultar, analizar datos y añadir registros.

## Funcionalidades

- Autenticación de usuario
- Menú lateral para navegar entre diferentes páginas  
- 3 Dashboards con gráficos y métricas interactivas
- Formularios para agregar nuevos libros, editoriales y distribuidoras
- Búsqueda de libros para ver métricas de compra y detalles

## Requisitos

- OPUS_HUB en SQL Server
- Python
- Streamlit  
- Pandas
- Pyodbc
- Plotly
- ...

## Configuración

1. Clonar la base de datos
2. Instalar requisitos con `pip install -r requirements.txt`
3. Configurar la cadena de conexión a la DB en `streamlit_app.py`
4. Ejecutar con `streamlit run streamlit_app.py`

## Archivos

- `streamlit_app.py`: Código principal de la aplicación
- `images/`: Imágenes y logos usados en la app
- `lottie_files/`: Animaciones
- `requirements.txt`: Dependencias de Python

## Usuario para acceder

User: admin
Password: admin
