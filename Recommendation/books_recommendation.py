import dynamodb_mapper
import boto3
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import pandas as pd
import os
import shutil
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from sklearn.neighbors import NearestNeighbors

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def download_and_convert_data(table , filename):
    data_downloaded = download_data(table)
    convert_to_csv(data_downloaded, filename)

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

def convert_to_csv(data_downloaded, filename):
    if data_downloaded is None:
        return
    if os.path.exists(filename):
        shutil.rmtree(filename, ignore_errors=True)
    with open(filename, 'w' ,encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=data_downloaded['keys'],quotechar='"')
        writer.writeheader()
        writer.writerows(data_downloaded['items'])

download_and_convert_data("hungrymind-mobilehub-593518188-Customer_table" , "user.csv")
download_and_convert_data("hungrymind-mobilehub-593518188-Books" , "books.csv")
download_and_convert_data("hungrymind-mobilehub-593518188-BookBorrow" , "borrowed.csv")

books = pd.read_csv('books.csv',sep = ',' ,error_bad_lines = False , encoding = 'latin-1')
users = pd.read_csv('user.csv',sep = ',' ,error_bad_lines = False , encoding = 'latin-1')
borrow = pd.read_csv('borrowed.csv',sep = ',' ,error_bad_lines = False , encoding = 'latin-1')

new_book = books.sort_values('Rating' , ascending = False)
book_without_genre = new_book.drop(['Genre'] , axis = 1) #to handle Null data
valid_books = book_without_genre.dropna()
top_rated = valid_books.head(10)
top_rated_id = top_rated.ISBN
print ('Top Rated books are :')
print(top_rated.BookName)

ratings = borrow.drop(['BorrowId','DateClaimToRet','SupplierID','DateOfBorrow','ActualRetDate'] , axis = 1)

rat_new = ratings[ratings.BookID.isin(books.ISBN)]
ratings_ex = rat_new[rat_new.Rating != 0]
rat_count = pd.DataFrame(ratings_ex.groupby('BookID')['Rating'].count())
rat_count.sort_values('Rating' , ascending = False ,inplace = True)
rat_count.head()

most_rated = books[books.ISBN.isin(rat_count.index)]
most_r = most_rated.head(10)
most_rat_Id = most_r.ISBN

print ('Most Rated Books are : ')
print (most_r.BookName)

r_matrix = ratings_ex.pivot_table(
    index='CustID',
    columns='BookID',
    values='Rating',
    aggfunc = np.mean
).fillna(0)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1)
model_knn.fit(r_matrix.T)

def item_similarity(isbn , rat):
    similarities = []
    indices = []
    rat = rat.T
    loc = rat.index.get_loc(isbn)
    distances ,indices = model_knn.kneighbors(rat.iloc[loc , :].values.reshape(1,-1))
    similarities = 1 - distances.flatten()
    return similarities, indices

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

recommend_id = books.ISBN[recommend.index]

#All the recommended book ids stored in arrays

print(recommend_id.head())
print(most_rat_Id.head())
print(top_rated_id.head())

