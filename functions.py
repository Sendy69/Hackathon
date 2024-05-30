#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df=pd.read_csv("dataset_hackathon/datasetreco.csv", sep=";")


# In[3]:


df.head()


# In[4]:


df.head(15)


# In[5]:


#df[df["user_id"]==1515915625519468736]


# In[6]:


df.duplicated().sum()


# In[7]:


df=df.drop_duplicates()


# In[8]:


df.columns


# In[ ]:





# In[9]:


df.info()


# In[10]:


analyse_df= df[['user_id','product_id','subsubcategory','is_view','is_cart','is_purchase','p_views','p_carts','p_purchases']]


# In[ ]:





# In[11]:


analyse_df['rating']=analyse_df['p_views']*1+analyse_df['p_carts']*5+analyse_df['p_purchases']*10
analyse_df


# In[12]:


df_purchased=analyse_df[df['p_purchases']>=1]
df_purchased=df_purchased[['user_id','product_id','subsubcategory','rating']]
normalized_dfs=[]
for _, group in df_purchased.groupby('subsubcategory'):
    max_rating = group['rating'].max()
    group['rating'] = group['rating'] / max_rating
    normalized_dfs.append(group)
    final_puchased_df= pd.concat(normalized_dfs)
final_puchased_df


# In[13]:


#final_puchased_df[final_puchased_df["user_id"]==1515915625611017316]


# In[14]:


final_puchased_df.duplicated().sum()


# In[15]:


df_purchased=final_puchased_df.drop_duplicates()
df_purchased


# In[16]:


pivot_table1 = df_purchased.pivot_table(
    values='rating', 
    index='product_id', 
    columns='user_id',
    fill_value=0
)
pivot_table1


# In[17]:


from sklearn.decomposition import TruncatedSVD
#from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# pivot_table_scaled = scaler.fit_transform(pivot_table1)
# pivot_table_scaled
# Utiliser Truncated SVD pour la réduction de dimension
svd = TruncatedSVD(n_components=10, random_state=7)
pivot_table_reduced = svd.fit_transform(pivot_table1)
sdv_df=pd.DataFrame(pivot_table_reduced, index=pivot_table1.index)
sdv_df
# # Calculer la matrice de corrélation

# # svd_df = pd.DataFrame(correlation_matrix, index=pivot_table1.index, columns=['product_id', 'product_id'])


# In[18]:


matrix = pd.DataFrame(sdv_df.T).corr()


# In[19]:


#matrix


# In[20]:


def recommend_products(product_id, correlation_matrix=matrix, top_n=10):
    if product_id not in correlation_matrix:
        return f"Le produit {product_id} n'est pas dans la matrice de corrélation."
    product_correlations = correlation_matrix[product_id]
    similar_products = product_correlations.sort_values(ascending=False)
    similar_products = similar_products.drop(product_id)
    return similar_products.head(top_n)


# In[21]:


#recommend_products(3727)


# In[22]:


#df[df["user_id"]==1515915625519407618].shape[0]


# In[23]:


def recommen_user_v1(id):
    user=df[df["user_id"]==id].iloc[[-1]]
    product=user["product_id"].array[0]
    list_recommend=recommend_products(product)
    return list_recommend


# In[36]:


#list=recommen_user_v1(1515915625519470612).astype(float)


# In[37]:


#list


# In[35]:


#list = recommen_user_v1(1515915625519470612)
#list


# In[26]:


list.index


# In[27]:


def recommen_user_v2(id):
    user_history=df[df["user_id"]==id]
    product_history=user_history["product_id"].array
    max_produit=0
    max_pond=0
    i=0
    for prod in product_history:
        if max_pond< sum(recommend_products(prod)*(product_history.shape[0]-i)/product_history.shape[0]):
            max_pond=sum(recommend_products(prod)*(product_history.shape[0]-i)/product_history.shape[0])
            max_produit=prod
    i=i+1
    recom_df=recommend_products(max_produit)
    # print(max_pond)
    # print(max_produit)
    recom_df=recom_df.sort_values(ascending=False).head(10)
    return recom_df


# In[28]:


list2=recommen_user_v2(1515915625519470612)
list2


# In[29]:


df[df['product_id']==3760003]


# In[ ]:




