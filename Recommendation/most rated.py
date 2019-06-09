from __future__ import print_function 
import boto3
import os

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
    books = data_downloaded['Items']
    table = dynamodb.Table("hungrymind-mobilehub-593518188-BookBorrow")
    data_downloaded2 = table.scan()
    borrow = data_downloaded2['Items']
    
    print(borrow)
    
    ratings =[]
    for item in borrow:
        ratings.append(item['Rating'],item['CustID'],item['BookID'])
    
    rat_new = ratings[ratings.BookID.isin(books.ISBN)]
    ratings_ex = rat_new[rat_new.Rating != 0]
    rat_count = pd.DataFrame(ratings_ex.groupby('BookID')['Rating'].count())
    rat_count.sort_values('Rating' , ascending = False ,inplace = True)
    rat_count.head()
    
    most_rated = books[books.ISBN.isin(rat_count.index)]
    most_r = most_rated.head(10)
    most_rat_Id = most_r.ISBN
    
    return most_rat_Id

    
if __name__ == '__main__':
    app.run()