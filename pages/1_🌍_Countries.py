import pandas as pd
import streamlit as st
import inflection
import plotly.express as px
import streamlit.components.v1 as components


df = pd.read_csv('data/zomato.csv')

st.set_page_config( page_title = "Home", page_icon="🌍", layout="wide")

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
                        # Functions
                        # ====================================
            
# Quantidade de Restaurantes Registrados por País
def QtdRestaurantes(df):
    df_aux = df1.groupby('country_name').count().sort_values(by='restaurant_id', ascending=False).reset_index()    
    fig = px.bar(df_aux, x=df_aux['country_name'], y=df_aux['restaurant_id'], color=df_aux['country_name'], labels={'country_name': 'Países', 'restaurant_id' : 'Quantidade de Restaurantes'}, text=df_aux['restaurant_id'])
    fig.update_layout(
    title='Quantidade de Restaurantes Registrados por País',
    title_x = 0.3,)
    st.plotly_chart(fig, use_container_width=True)
    
# Quantidade de Cidades Registradas por País
def QtdCidades(df):
    df_aux = df1.groupby('country_name')['city'].nunique().sort_values(ascending=False).reset_index()   
    fig = px.bar(df_aux, x=df_aux['country_name'], y=df_aux['city'], color=df_aux['country_name'], labels={'country_name': 'Países', 'city' : 'Quantidade de Cidades'}, text=df_aux['city'])
    fig.update_layout(
    title='Quantidade de Cidades Registradas por País',
    title_x = 0.3,)
    st.plotly_chart(fig, use_container_width=True)
    
# Media de preco de prato para duas pessoas por País
def AvarageCostForTwo(df):
    df_aux = df1.groupby('country_name')['average_cost_for_two'].median().reset_index().sort_values(by= 'average_cost_for_two' ,ascending=False)
    fig = px.bar(df_aux, x=df_aux['country_name'], y=df_aux['average_cost_for_two'], color=df_aux['country_name'], labels={'country_name': 'Países', 'average_cost_for_two' : 'Preço de prato para duas pessoas'}, text=df_aux['average_cost_for_two'])
    fig.update_layout(
    title='Média de preço de um prato para duas pessoas por País',
    title_x = 0.1,)
    st.plotly_chart(fig, use_container_width=True)
    

# Media de avaliacoes por País
def AvarageForCountry(df):
    df_aux = round(df1.groupby('country_name')['votes'].mean().reset_index()).sort_values(by= 'votes' ,ascending=False)
    fig = px.bar(df_aux, x=df_aux['country_name'], y=df_aux['votes'], color=df_aux['country_name'], labels={'country_name': 'Países', 'votes' : 'Quantidade de Avaliações'}, text=df_aux['votes'])
    fig.update_layout(
    title='Média de Avaliações feitas por País',
    title_x = 0.2,)
    st.plotly_chart(fig, use_container_width=True)
    

            
            

                        # ====================================
                        # Barra Lateral do streamlit
                        # ====================================                 

st.sidebar.markdown("## Filtros:")


countries_options = st.sidebar.multiselect (
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Brazil', 'England', 'Qatar', 'South Africa','Canada', 'Australia'] )




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
            
            
            
st.markdown("# 🌍 Visão por Países")

with st.container():
    QtdRestaurantes(df1)
    
with st.container():
    QtdCidades(df1)
    

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        AvarageForCountry(df1)
    
    with col2:
        AvarageCostForTwo(df1)