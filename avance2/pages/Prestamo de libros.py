import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Informacion de Libros',
                   page_icon='books',
                   layout="wide")


st.title(':books: Informacion de Libros')
st.subheader('¿Los tipos de libros que se puede encontran en nuestra libreria?')

archivo_excel = 'C:/avance2/Tipo de libros.xlsx'
hoja_excel = 'Tipo de libros'

df_prestamo = pd.read_excel(archivo_excel, sheet_name=hoja_excel, usecols=list(range(2, 18)))


st.sidebar.header("opciones de filtro de tabla")
SECTOR=st.sidebar.multiselect(
    "seleccione el sector:",
    options = df_prestamo['SECTOR'].unique(),
    default = df_prestamo['SECTOR'].unique()
)

FORMATO=st.sidebar.multiselect(
    "seleccione el formato:",
    options = df_prestamo['FORMATO'].unique(),
    default = df_prestamo['FORMATO'].unique()
)

DEPARTAMENTO_EDICION=st.sidebar.multiselect(
    "seleccione el departamento:",
    options = df_prestamo['DEPARTAMENTO_EDICION'].unique(),
    default = df_prestamo['DEPARTAMENTO_EDICION'].unique()
)

df_opcion = df_prestamo.query("SECTOR == @SECTOR &  FORMATO == @FORMATO & DEPARTAMENTO_EDICION == @DEPARTAMENTO_EDICION" )


st.dataframe(df_opcion)
st.markdown("---------------------")


precios =df_prestamo.groupby(['SECTOR'],as_index = False)['CANTIDAD_EJEMPLARES_ENTREGADOS'].count()


fig = px.pie(precios, values='CANTIDAD_EJEMPLARES_ENTREGADOS', names='SECTOR',
             title='Cantidad de ejemplares entregados por sector',
             hole=0.5,
)

st.plotly_chart(fig, use_container_width= True)

st.subheader("Cantidad de libros digitales y fisicos")
df_departamento = df_opcion.groupby('FORMATO')['TITULO'].count()
st.bar_chart(df_departamento)


