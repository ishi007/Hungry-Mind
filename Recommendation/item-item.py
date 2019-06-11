from __future__ import print_function 
import boto3
import os
import pandas as pd
from flask import Flask
from pandas.io.json import json_normalize
import numpy as np
from sklearn.neighbors import NearestNeighbors

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
    
    ratings = borrow.drop(['BorrowId','DateClaimToRet','SupplierID','DateOfBorrow','ActualRetDate'] , axis = 1)
    
    rat_new = ratings[ratings.BookID.isin(books.ISBN)]
    ratings_ex = rat_new[rat_new.Rating != 0]
    
    ratings_ex.Rating = ratings_ex.Rating.astype(float)
    
    r_matrix = ratings_ex.pivot_table(
        index='CustID',
        columns='BookID',
        values='Rating'
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
    uid = 1200
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
    
    ir = ""

    for i in range(len(recommend)):
        ir = ir + str(books.ISBN[recommend.index[i]]) + "<br>"
        
    return ir

if __name__ == '__main__':
    app.run(debug=True)

