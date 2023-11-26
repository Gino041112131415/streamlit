import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Informacion de Libros',
                   page_icon='books',
                   layout="wide")

st.title(':books: Informacion de Libros')
st.subheader('¿Qué libros aprobados se encuentran en librerías?')
st.sidebar.image("imagen/logo.png")

archivo_excel = 'Editoriales_aprobados.xlsx'
hoja_excel = 'BASE DE DATOS'


df_libros = pd.read_excel(archivo_excel, sheet_name=hoja_excel, usecols=list(range(4, 14)))

df_libros.dropna(axis=1)

st.sidebar.header("opciones de filtro de tabla")
DEPARTAMENTO_SOLICITANTE=st.sidebar.multiselect(
    "seleccione el departamento:",
    options = df_libros['DEPARTAMENTO_SOLICITANTE'].unique(),
    default = df_libros['DEPARTAMENTO_SOLICITANTE'].unique()
)

DISTRITO_SOLICITANTE=st.sidebar.multiselect(
    "seleccione el distrito:",
    options = df_libros['DISTRITO_SOLICITANTE'].unique(),
    default = df_libros['DISTRITO_SOLICITANTE'].unique()
)

NOMBRES_SOLICITANTE=st.sidebar.multiselect(
    "seleccione el solicitante:",
    options = df_libros['NOMBRES_SOLICITANTE'].unique(),
    default = df_libros['NOMBRES_SOLICITANTE'].unique()
)

df_opcion = df_libros.query("DEPARTAMENTO_SOLICITANTE == @DEPARTAMENTO_SOLICITANTE &  DISTRITO_SOLICITANTE == @DISTRITO_SOLICITANTE   &  NOMBRES_SOLICITANTE == @NOMBRES_SOLICITANTE ")

libro_max_copias = df_opcion.iloc[df_opcion['TIRAJE'].idxmax()]
titulo_libro_max_copias = libro_max_copias['TITULO']
distritos = df_opcion.iloc[df_opcion['DISTRITO_SOLICITANTE'].idxmax(), df_opcion.columns.get_loc('DISTRITO_SOLICITANTE')]


left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Distritos con mas pedidos:")
    st.subheader(f"{distritos}")

with right_column:
    st.subheader("libro con mas copias producidas:")
    st.subheader(f" libro {titulo_libro_max_copias}, Copias producidas {libro_max_copias['TIRAJE']}")

st.markdown("---------------------")
st.dataframe(df_opcion)


#para realizar la grafica de tablas de barra


libros = (df_opcion.groupby(by=['DISTRITO_SOLICITANTE'])).sum()[['TIRAJE']].sort_values(by="TIRAJE")

fig_libro=px.bar(
    libros,
    x='TIRAJE',
    y=libros.index,
    orientation='h',
    title="<b> cantidad de libros aprovados <b> ",
    color_discrete_sequence=["#0000FF"] * len(libros),
     template='plotly_white',
)

libros2 = (df_opcion.groupby(by=['NOMBRES_SOLICITANTE'])).sum()[['TITULO']].sort_values(by="TITULO")
fig_libro_2 = px.bar(
    libros2,
    x='TITULO',
    y=libros2.index,
    orientation='v',
    title="<b>    Titulos aprobados   <b>",
    color_discrete_sequence=["#0000FF"] * len(libros2),
    template='plotly_white',
    category_orders={"y": libros2.index}
)
ticktext = libros2['TITULO'].apply(lambda x: x[:14] + '...' if len(x) > 14 else x)
fig_libro_2.update_xaxes(tickangle=40, tickmode='array', tickvals=libros2['TITULO'], ticktext=ticktext)

st.subheader("Distribución de Títulos por Departamento")
df_departamento = df_opcion.groupby('DEPARTAMENTO_SOLICITANTE')['TITULO'].count()
st.bar_chart(df_departamento)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_libro, use_container_width= True)
right_column.plotly_chart(fig_libro_2, use_container_width= True)










