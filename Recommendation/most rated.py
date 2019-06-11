from __future__ import print_function 
import boto3
import os
import pandas as pd
from flask import Flask
from pandas.io.json import json_normalize
import numpy as np

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
os.environ["NO_PROXY"] = "s3.amazonaws.com"
app = Flask(__name__)

@app.route('/')
def page():
    return "Add /most"

@app.route('/most/')
def most_rated_books():
    
    table = dynamodb.Table("hungrymind-mobilehub-593518188-Books")
    data_downloaded = table.scan()
    table = dynamodb.Table("hungrymind-mobilehub-593518188-Book_Borrow")
    data_downloaded2 = table.scan()

    books = pd.DataFrame.from_dict(json_normalize(data_downloaded['Items']))
    borrow = pd.DataFrame.from_dict(json_normalize(data_downloaded2['Items']))
    
    ratings = borrow.drop(['BorrowId','DateClaimToRet','SupplierID','DateOfBorrow','ActualRetDate'],axis=1 )

    rat_new = ratings[ratings.BookID.isin(books.ISBN)]
    ratings_ex = rat_new[rat_new.Rating != 0]
    rat_count = pd.DataFrame(ratings_ex.groupby('BookID')['Rating'].count())
    rat_count.sort_values('Rating' , ascending = False ,inplace = True)
    
    most_rated = books[books.ISBN.isin(rat_count.index)]
    most_r = most_rated.head(10)
    most_rat_URL = ""
    
    #print ('Most Rated Books are : ')
    #print (most_r.BookName)
    
    mr = []
    mr = np.asarray(most_r.to_records(index=False))

    for i in range(0,10):
        most_rat_URL = most_rat_URL + str(mr[i][4])+" <br> "
    #print (most_rat_URL)
    
    return most_rat_URL

   
if __name__ == '__main__':
    app.run()
