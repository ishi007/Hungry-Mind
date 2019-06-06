#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dynamodb_mapper
import boto3
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import pandas as pd
import os
import click
import shutil
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from sklearn.neighbors import NearestNeighbors


# In[2]:


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


# In[3]:


def download_and_convert_data(table , filename):
    data_downloaded = download_data(table)
    convert_to_csv(data_downloaded, filename)


# In[4]:


def download_data(table_name):
    table = dynamodb.Table(table_name)
    key = []
    for obj in table.attribute_definitions:
        key.append(obj['AttributeName'])
    set_of_key = set(key)
    item_count = table.item_count

    data_downloaded = table.scan()
    if data_downloaded is None:
        return None

    items = data_downloaded['Items']
    column_names = set([])
    for item in items:
        column_names = column_names.union(set(item.keys()))
    print(column_names)
    print("Total downloaded records: ",len(items))

    for c_name in column_names:
        if c_name not in set_of_key:
            key.append(c_name)
    return {'items': items, 'keys': key}


# In[5]:


def convert_to_csv(data_downloaded, filename):
    if data_downloaded is None:
        return
    if os.path.exists(filename):
        shutil.rmtree(filename, ignore_errors=True)
    with open(filename, 'w' ,encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=data_downloaded['keys'],quotechar='"')
        writer.writeheader()
        writer.writerows(data_downloaded['items'])


# In[6]:


download_and_convert_data("hungrymind-mobilehub-593518188-Customer_table" , "user.csv")


# In[7]:


download_and_convert_data("hungrymind-mobilehub-593518188-Books" , "books.csv")


# In[8]:


download_and_convert_data("hungrymind-mobilehub-593518188-BookBorrow" , "borrowed.csv")


# In[9]:


books = pd.read_csv('books.csv',sep = ',' ,error_bad_lines = False , encoding = 'latin-1')
users = pd.read_csv('user.csv',sep = ',' ,error_bad_lines = False , encoding = 'latin-1')
borrow = pd.read_csv('borrowed.csv',sep = ',' ,error_bad_lines = False , encoding = 'latin-1')


# In[10]:


borrow.head()


# In[11]:


books.head()


# In[12]:


users.head()


# In[13]:


new_book = books.sort_values('Rating' , ascending = False)
new_book.head()


# In[14]:


book_without_genre = new_book.drop(['Genre'] , axis = 1)


# In[15]:


valid_books = book_without_genre.dropna()


# In[16]:


top_rated = valid_books.head(10)
top_rated_id = top_rated.ISBN


# In[17]:


print ('Top Rated books are :')
top_rated.BookName


# In[18]:


borrow.head()


# In[19]:


ratings = borrow.drop(['BorrowId','DateClaimToRet','SupplierID','DateOfBorrow','ActualRetDate'] , axis = 1)


# In[20]:


ratings.head()


# In[21]:


ratings.shape


# In[22]:


rat_new = ratings[ratings.BookID.isin(books.ISBN)]
rat_new = rat_new[rat_new.CustID.isin(users.userId)]
rat_new.shape


# In[23]:


ratings_ex = rat_new[rat_new.Rating != 0]
rat_count = pd.DataFrame(ratings_ex.groupby('BookID')['Rating'].count())
rat_count.sort_values('Rating' , ascending = False ,inplace = True)
rat_count.head()


# In[24]:


most_rated = books[books.ISBN.isin(rat_count.index)]
most_r = most_rated.head(10)
most_rat_Id = most_r.ISBN


# In[25]:


print ('Most Rated Books are : ')
most_r.BookName


# In[26]:


ratings_ex.head()


# In[27]:


r_matrix = ratings_ex.pivot_table(
    index='CustID',
    columns='BookID',
    values='Rating',
    aggfunc = np.mean
).fillna(0)


# In[28]:


model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1)


# In[29]:


model_knn.fit(r_matrix.T)


# In[30]:


def item_similarity(isbn , rat):
    similarities = []
    indices = []
    rat = rat.T
    loc = rat.index.get_loc(isbn)
    distances ,indices = model_knn.kneighbors(rat.iloc[loc , :].values.reshape(1,-1))
    similarities = 1 - distances.flatten()
    return similarities, indices


# In[31]:


def predict_item(uid , isbn , rat):
    prediction = w_sum = 0
    uloc = rat.index.get_loc(uid)
    itloc = rat.columns.get_loc(isbn)
    similarities , indices = item_similarity(isbn , rat)
    sum_of_similarities = np.sum(similarities) - 1
    if sum_of_similarities == 0:
        sum_of_similarities = 1
    product = 1
    for i in range(0 , len(indices.flatten())):
        if indices.flatten()[i] == itloc:
            continue;
        else:
            product = rat.iloc[uloc,indices.flatten()[i]]
            product = product*(similarities[i])
            w_sum = w_sum + product
            
    prediction = round(w_sum/sum_of_similarities)
    if prediction <=0:
        prediction = 1
    elif prediction >10:
        prediction = 10

    return prediction


# In[32]:


#Takes user input
#In the app it will be the id of logged in user
uid = int(input(""))
rat = r_matrix
predi = []
for i in range(rat.shape[1]):
    if (rat[rat.columns[i]][uid] != 0):
        predi.append(predict_item(uid , rat.columns[i], rat))
    else:
        predi.append(-1)
predi = pd.Series(predi)
predi = predi.sort_values(ascending = False)
recommend = predi[:10]
print ("Recommended books are: ")
for o in range(len(recommend)):
    print ( o+1 ,'.' , books.BookName[recommend.index[o]])


# In[33]:


recommend_id = books.ISBN[recommend.index]


# In[34]:


#All the recommended book ids stored in arrays


# In[35]:


recommend_id.head()


# In[36]:


most_rat_Id.head()


# In[37]:


top_rated_id.head()


# In[ ]:




