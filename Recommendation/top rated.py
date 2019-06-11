from __future__ import print_function 
import boto3
import os
from flask import Flask
from pandas.io.json import json_normalize
import numpy as np
import pandas as pd

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
os.environ["NO_PROXY"] = "s3.amazonaws.com"

app = Flask(__name__)

@app.route('/')
def page():
    return "Add /top"

@app.route('/top/')
def top_rated_books():
    
    table = dynamodb.Table("hungrymind-mobilehub-593518188-Books")
    downloaded_data = table.scan()
    
    books = pd.DataFrame.from_dict(json_normalize(downloaded_data['Items']))
    new_book = books.sort_values('Rating' , ascending = False)
    book_without_genre = new_book.drop(['Genre'] , axis = 1) #to handle Null data
    valid_books = book_without_genre.dropna()
    top_rated = valid_books.head(10)
    #print ('Top Rated books are :')
    #print(top_rated.BookName)
    
    tr = []
    tr = np.asarray(top_rated.to_records(index=False))
    top_rated_URL = ""
    
    for i in range(0,10):
        top_rated_URL = top_rated_URL + str(tr[i][3])+" <br>"
    #print (top_rated_URL)
    
    return top_rated_URL

    
if __name__ == '__main__':
    app.run()
