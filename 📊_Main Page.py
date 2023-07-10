import pandas as pd
import inflection
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import streamlit.components.v1 as components


df = pd.read_csv('data/zomato.csv')

#st.set_page_config(layout="wide")
st.set_page_config( page_title = "Home", page_icon="📊", layout="wide")

                        # ====================================
                        # Limpeza DataFrame
                        # ====================================

# Renomeando Colunas
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x) 
    snakecase = lambda x: inflection.underscore(x) 
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old)) 
    cols_old = list(map(spaces, cols_old)) 
    cols_new = list(map(snakecase, cols_old)) 
    df.columns = cols_new
    return df

df1 = rename_columns(df)

# Removendo duplicadas
df1 = df1.drop_duplicates()

# Removendo coluna Switch to order menu que possui linhas com apenas 1 valor
df1 = df1.drop('switch_to_order_menu', axis=1)

# Removendo linhas NULL (NaN)
df1 = df1.dropna()

## Removendo valores multiplos (Filipino, American, Italian, Bakery) da coluna 'Cuisines'
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

#Coluna Country Name
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES.get(country_id)

df1['country_name'] = df1['country_code'].apply(country_name)

# Coluna Price Type
def create_price_type(price_range):
    if price_range == 1: return "cheap"
    elif price_range == 2: return "normal"
    elif price_range == 3: return "expensive"
    else:
        return "gourmet"

df1['price_type'] = df1['price_range'].apply(create_price_type)


# Coluna Color Name
COLORS = {
   "3F7E00": "darkgreen",
   "5BA829": "green",
   "9ACD32": "lightgreen",
   "CDD614": "orange",
   "FFBA00": "red",
   "CBCBC8": "darkred",
   "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

df1['color_name'] = df1['rating_color'].apply(color_name)


                        # ====================================
                        # Barra Lateral do streamlit
                        # ====================================

image = Image.open('food.png')
            
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 40%;
        }
    </style>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.image(image)

st.sidebar.markdown("<h1 style='text-align: center;'><i>Fome Zero Delivery</i></h1>", unsafe_allow_html=True) 
                    

st.sidebar.markdown("## Filtros:")


countries_options = st.sidebar.multiselect (
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Brazil', 'England', 'Qatar', 'South Africa','Canada', 'Australia'] )



# Bottom Download
st.sidebar.markdown("## Dados tratados:")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df1)


st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)



# ADICIONAR PERFIL LINKEDIN
st.sidebar.markdown("## Contato:")
with st.sidebar:
    components.html("""
                    <div class="badge-base LI-profile-badge" data-locale="pt_BR" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="dslucasribeiro" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/dslucasribeiro?trk=profile-badge"></a></div>
                    <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>              
              """, height= 310)
              


# HABILITAR FILTRO:
line_countries_options = df1.loc[:, 'country_name'].isin(countries_options)
df1 = df1.loc[line_countries_options,:]

                        # ====================================
                                    # DASHBOARD
                        # ====================================
st.write("# Fome Zero Delivery Dashboard")
st.markdown("## O Melhor lugar para encontrar seu mais novo restaurante favorito!")
st.markdown("### Temos as seguintes marcas dentro da nossa plataforma: ")

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        df_aux = df1['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', df_aux)
        
    with col2:
        df_aux = df1['country_code'].nunique()
        col2.metric('Países Cadastrados', df_aux)
        
    with col3:
        df_aux = df1['city'].nunique()
        col3.metric('Cidades Cadastradas', df_aux)
        
    with col4:
        num = df1['votes'].sum()
        numero_formatado = "{:,}".format(num).replace(",", ".")
        col4.metric('Avaliações Realizadas', numero_formatado)
        
    with col5:
        df_aux = df1['cuisines'].nunique()
        col5.metric('Tipos de Culinárias oferecidas', df_aux)
        
with st.container():
    map = folium.Map()
    cluster = MarkerCluster().add_to(map)
    cols = ['restaurant_name', 'latitude','longitude', 'average_cost_for_two', 'cuisines', 'aggregate_rating', 'country_name']
    df_aux = df1.loc[:, cols]
    
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['latitude'], location_info['longitude']],
                    popup="{} Preço para dois: {} Type: {}  Nota Agregada: {}".format(location_info['restaurant_name'], location_info['average_cost_for_two'], location_info['cuisines'], location_info['aggregate_rating']), icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(cluster)

        
folium_static (map, width = 1024, height=600 )
        
    
