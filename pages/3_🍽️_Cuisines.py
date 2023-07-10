import pandas as pd
import streamlit as st
import inflection
import plotly.express as px
import streamlit.components.v1 as components


df = pd.read_csv('data/zomato.csv')

st.set_page_config( page_title = "Cuisines", page_icon="🍽️", layout="wide")

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

df_graph = df1.copy()

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


date_slider = st.sidebar.slider(
    'Selecione a quantidade de Restaurantes que deseja visualizar',
    value=10,
    min_value=1,
    max_value=20)

cuisines_options = st.sidebar.multiselect (
    'Escolha os Principais Tipos de Culinária',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],
default=['Brazilian', 'Italian', 'American', 'Arabian','Japanese'] )

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

df1.head(date_slider)

line_cuisines_options = df1.loc[:, 'cuisines'].isin(cuisines_options)
df1 = df1.loc[line_cuisines_options, :]


                        # ====================================
                        # Functions
                        # ====================================
            
# Metricas principais
def Metrics(df, op, col):
    line1 = df1.loc[:, 'cuisines'] == cuisines_options[op]
    df2 = df1.loc[line1, :]
    max = df2.loc[:,'aggregate_rating'].max()
    line2 = df2.loc[:, 'aggregate_rating'] == max
    df3 = df2.loc[line2,:]
    min = df3.loc[:,'restaurant_id'].min()
    line3 = df3.loc[:, 'restaurant_id'] == min
    df_final = df3.loc[line3,:]
    col.metric("{}: {}".format(df_final['cuisines'].values[0], df_final['restaurant_name'].values[0]), "{}/5.0".format(df_final['aggregate_rating'].values[0]), help="País: {} / Cidade: {} / Média de Prato para dois: {} ".format(df_final['country_name'].values[0], df_final['city'].values[0], df_final['average_cost_for_two'].values[0]))

    
# Top 10 Restaurantes (tabela)
def Top10restaurants(df):
    line = df1.loc[:, 'aggregate_rating'] == 4.9
    df1['restaurant_id'] = df1['restaurant_id'].astype(str)
    df_aux = df1.loc[line, ['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']].sort_values(by='restaurant_id', ascending = True).head(date_slider)
    st.dataframe(df_aux)
    
    
    

# Top 10 Melhores Tipos de Culinárias (grafico)
def CuisinesType(df, tipo):
    df_grouped = df_graph.groupby('cuisines').aggregate_rating.mean().reset_index().head(date_slider)
    df_grouped = df_grouped.sort_values(by='aggregate_rating', ascending=tipo)
    fig = px.bar(df_grouped, x='cuisines', y='aggregate_rating', 
             labels={'cuisines': 'Culinária', 'aggregate_rating': 'Avaliação Média'}, text=round(df_grouped['aggregate_rating'],2))

    fig.update_layout(title='Top {} Melhores Tipos de Culinárias'.format(date_slider), title_x=0.3)
    st.plotly_chart(fig, use_container_width=True)

    
    

                        # ====================================
                                    # DASHBOARD
                        # ====================================
            
            
            
st.markdown("# 🏙️ Visão por Tipo de Culinária")

with st.container():
    st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        try:
            Metrics(df1, 0, col1)
        except Exception as e:
            st.markdown("")
            
    with col2:
        try:
            Metrics(df1, 1, col2)
        except Exception as e:
            st.markdown("")
            
    with col3:
        try:
            Metrics(df1, 2, col3)
        except Exception as e:
            st.markdown("")
            
    with col4:
        try:
            Metrics(df1, 3, col4)
        except Exception as e:
            st.markdown("")

    with col5:
        try:
             Metrics(df1, 4, col5)
        except Exception as e:
            st.markdown("")

        
with st.container():
        st.markdown('## Top {} Restaurantes'.format(date_slider))
        Top10restaurants(df1)
        
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        CuisinesType(df1, False)
    with col2:
        CuisinesType(df1, True)



    

