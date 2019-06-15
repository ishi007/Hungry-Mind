from __future__ import print_function 
import boto3
import os
import pandas as pd
from flask import Flask
from pandas.io.json import json_normalize
from datetime import datetime
from statistics import mean 
from datetime import timedelta


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

os.environ["NO_PROXY"] = "s3.amazonaws.com"
app = Flask(__name__)

@app.route('/')
def page():
    return "Add /item/userid/bookid"

@app.route('/item/<u_id>/<b_id>',methods=['GET'])
def most_rated_books(u_id,b_id):

    table = dynamodb.Table("hungrymind-mobilehub-593518188-Book_Borrow")
    data_downloaded = table.scan()
    borrow = pd.DataFrame.from_dict(json_normalize(data_downloaded['Items']))
    borrow.drop(['CustId'],axis=1,inplace=True)
    
    user_records = borrow.drop(['BorrowId','BookID','Rating','SupplierID'] , axis = 1)
    book_records = borrow.drop(['BorrowId','CustID','Rating','SupplierID'] , axis = 1)

    current_user = int(u_id)
    curr_user_records = user_records[user_records.CustID == current_user]
    curr_user_records.drop(['CustID'] , axis = 1 ,inplace=True)
    
    current_book = int(b_id)
    curr_book_records = book_records[book_records.BookID == current_book]
    curr_book_records.drop(['BookID'] , axis = 1 ,inplace=True)

    to_be_predicted = curr_book_records[curr_book_records['ActualRetDate'].isnull()]
  
    curr_book_records.dropna(inplace=True)
    curr_user_records.dropna(inplace=True)
    
    date = to_be_predicted.DateClaimToRet.values
    datestr = str(date[0])
    curr_date_claim = datetime.strptime(datestr, '%d-%m-%Y')
    
    def find_average(records):
        actual_date = []
        claimed_date = []
    
        for i in range(len(records)):
            actual_date.append(records.iloc[i,:].ActualRetDate)
            claimed_date.append(records.iloc[i,:].DateClaimToRet)
            
        difference = []
        for i in range(len(actual_date)):
            ad = datetime.strptime(str(actual_date[i]), '%d-%m-%Y')
            cd = datetime.strptime(str(claimed_date[i]), '%d-%m-%Y')
            difference.append(int((cd-ad).days))
         
        average = mean(difference)  
        return average

    average_cust = find_average(curr_user_records)
    average_book = find_average(curr_book_records)
    print(average_cust,average_book)

    w1 = 0.5
    w2 = 0.5
    total_avg = (w1*average_cust)+(w2*average_book)
    total_avg = round(total_avg/(w1+w2))

    predicted_date = curr_date_claim - timedelta(days=round(total_avg))
    predicted_date_str = str(predicted_date.day)+"-"+str(predicted_date.month)+"-"+str(predicted_date.year)
    
    return predicted_date_str

if __name__ == '__main__':
    app.run(debug=True)

