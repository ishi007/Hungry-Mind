from __future__ import print_function 
import boto3
import os
import pandas as pd
from flask import Flask
from pandas.io.json import json_normalize
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

os.environ["NO_PROXY"] = "s3.amazonaws.com"
app = Flask(__name__)

@app.route('/')
def page():
    return "Add /item/userid"

@app.route('/item/<u_id>',methods=['GET'])
def most_rated_books(u_id):

    table = dynamodb.Table("hungrymind-mobilehub-593518188-Books")
    data_downloaded = table.scan()
    table = dynamodb.Table("hungrymind-mobilehub-593518188-Book_Borrow")
    data_downloaded2 = table.scan()
    
    books = pd.DataFrame.from_dict(json_normalize(data_downloaded['Items']))
    borrow = pd.DataFrame.from_dict(json_normalize(data_downloaded2['Items']))
    
    books.drop(['Genre'] , axis = 1 ,inplace=True)
    books.columns
    
    ratings = borrow.drop(['BorrowId','DateClaimToRet','SupplierID','DateOfBorrow','ActualRetDate'] , axis = 1)
    
    rat_new = ratings[ratings.BookID.isin(books.ISBN)]
    ratings_ex = rat_new[rat_new.Rating != 0]
    
    ratings_ex.Rating = ratings_ex.Rating.astype(float)
    
    r_matrix = ratings_ex.pivot_table(
        index='CustID',
        columns='BookID',
        values='Rating'
        ).fillna(0)
    
    
    tfidf_vectorizer=TfidfVectorizer()
    def dist(a,b):
        dista = 0
        b1 = books.loc[books.ISBN == a ]
        b2 = books.loc[books.ISBN == b ]
        text = (str(b1.BookName) , str(b2.BookName))
        tfidf_matrix=tfidf_vectorizer.fit_transform(text)
        dista = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix)
        return dista
    
    
    def predict_item(uid , isbn , rat,indices,similarities):
        prediction = w_sum = 0
        
        for i in range(len(similarities[0])):
            if similarities[0][i] == 1:
                continue
            else:
                sum_of_similarities = similarities[0][i]
    
        if sum_of_similarities == 0:
            sum_of_similarities = 1
        product = 1
        
        for i in range(len(indices)):
            product = indices[i][0]
            product = product*(similarities[0][i+1])
            w_sum = w_sum + product
        
        prediction = (w_sum/sum_of_similarities)
        if prediction <=0:
            prediction = 1
        elif prediction >5:
            prediction = 5
    
        return prediction
    
    def user_data(uid,isbn,rat):
        values = []
        similarities = []
        loc = rat.index.get_loc(uid)
        arr = rat.iloc[: , loc].values.reshape(rat.shape[0])
        arr2 = arr[np.nonzero(arr)]
        
        if len(arr2)>0:
            for elements in arr2:
                values.append(arr[np.where(arr==elements)])
                similarities = dist(isbn,elements)
    
            return predict_item(uidd ,isbn, rat ,values,similarities)
        else:
            return 1
    
    uidd = int(u_id)
    rat = r_matrix
    predi = []
    
    for i in range(rat.shape[1]):
        if (rat[rat.columns[i]][uidd] == 0):
            predi.append(int(user_data(uidd,rat.columns[i],rat)))
        else:
            predi.append(-1)
    
    
    predi = pd.Series(predi)
    predi = predi.sort_values(ascending = False)
    recommend = predi[:10]
    
    ir = ""

    for i in range(len(recommend)):
        ir = ir + str(books.ISBN[recommend.index[i]]) + "<br>"
        
    return ir

if __name__ == '__main__':
    app.run()

