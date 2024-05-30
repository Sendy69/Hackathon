import streamlit as st
import pandas as pd
import plotly.express as px
# Charger la fonction recommend_v2
from functions import * 
# Charger ou préparer les données nécessaires


df = pd.read_csv('dataset_hackathon\datasetreco.csv', sep=";")
# Vous devez vous assurer que le même DataFrame est utilisé ici comme dans le notebook

# Simuler la matrice de corrélation pour cet exemple
# Vous devez charger la matrice de corrélation calculée dans le notebook
# Par exemple: correlation_matrix = pd.read_pickle('correlation_matrix.pkl')
# Interface utilisateur Streamlit
st.title('Product Recommendation System')
Aff_df=df_purchased.head(25)
st.write(Aff_df)

user_id = int(st.text_input('Enter User ID:'))
recommendation=st.button('Recommend')


st.write("Recommendation V1")
if recommendation:
    if user_id:
        st.write('Recommended Products for user: '+str(user_id))
        recommendations = recommen_user_v1(int(user_id))
        st.write(recommendations)
        result_count_dataframes = []
        result_dataframes=[]
# Parcourir chaque product_id dans A
        for product_id in recommendations.index:
            # Filtrer les lignes de df pour le product_id courant
            product_data = df[df['product_id'] == product_id]
            product_data['date'] = pd.to_datetime(product_data['Date'])
            if not product_data.empty:
                # Compter les occurrences par jour
                product=product_data
                daily_counts = product_data.groupby(product_data['date'].dt.date).size().reset_index(name='count')
                daily_counts['product_id'] = product_id  # Ajouter le product_id au DataFrame
                
                # Ajouter le DataFrame résultant à la liste
                result_count_dataframes.append(daily_counts)
                result_dataframes.append(product)
        # Combiner tous les DataFrames de résultats
        all_counts = pd.concat(result_count_dataframes)   
        all_product=pd.concat(result_dataframes)  
        all_product=all_product[["product_id","price","category","subcategory","subsubcategory"]]
        all_product=all_product.drop_duplicates()
        st.write(all_product)
        # Créer le graphique
        fig = px.line(all_counts, x='date', y='count', color='product_id', title='Product Interaction Count by Date')

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig)
    else:
        st.write('Please enter a valid Product ID.')


st.write("Recommendation V2")
if recommendation:
    if user_id:
        st.write('Recommended Products for user: '+str(user_id))
        recommendations = recommen_user_v2(int(user_id))
        st.write(recommendations)
        result_count_dataframes = []
        result_dataframes=[]
# Parcourir chaque product_id dans A
        for product_id in recommendations.index:
            # Filtrer les lignes de df pour le product_id courant
            product_data = df[df['product_id'] == product_id]
            product_data['date'] = pd.to_datetime(product_data['Date'])
            if not product_data.empty:
                # Compter les occurrences par jour
                product=product_data
                daily_counts = product_data.groupby(product_data['date'].dt.date).size().reset_index(name='count')
                daily_counts['product_id'] = product_id  # Ajouter le product_id au DataFrame
                
                # Ajouter le DataFrame résultant à la liste
                result_count_dataframes.append(daily_counts)
                result_dataframes.append(product)
        # Combiner tous les DataFrames de résultats
        all_counts = pd.concat(result_count_dataframes)   
        all_product=pd.concat(result_dataframes)  
        all_product=all_product[["product_id","price","category","subcategory","subsubcategory"]]
        all_product=all_product.drop_duplicates()
        st.write(all_product)
        # Créer le graphique
        fig = px.line(all_counts, x='date', y='count', color='product_id', title='Product Interaction Count by Date')

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig)
    else:
        st.write('Please enter a valid Product ID.')


if user_id:
    # Filtrer les données pour l'utilisateur donné
    user_data = df[df['user_id'] == int(user_id)]
    st.write(user_data)
    if not user_data.empty:
        # Compter les interactions par date
        user_data['date'] = pd.to_datetime(user_data['Date'])
        activity_over_time = user_data.groupby([user_data['date'].dt.date,'event_type']).size().reset_index(name='count')
        
        # Créer le graphique
        fig = px.histogram(activity_over_time, x='date', y='count', color='event_type',title='User Activity Over Time')
        st.plotly_chart(fig)
    else:
        st.write('No data available for this User ID.')

