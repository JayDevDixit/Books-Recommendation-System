from flask import Flask,render_template,request
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

def find_popular_books():
    books = pd.read_csv('Books.csv')
    book_rating = pd.read_csv('Book-Rating.csv')
    num_rating = book_rating.groupby('Book-Title').count()['Book-Rating'].reset_index()
    num_rating.rename(columns={'Book-Rating':'Num-Rating'},inplace=True)
    avg_rating = book_rating.groupby('Book-Title').mean()['Book-Rating'].reset_index()
    avg_rating.rename(columns={'Book-Rating':'Avg-Rating'},inplace=True)
    popular_books = num_rating.merge(avg_rating,on='Book-Title')
    popular_books = popular_books[popular_books['Num-Rating']>=250]
    popular_books.sort_values('Avg-Rating',ascending=False,inplace=True)
    popular_books = popular_books.merge(books,on='Book-Title').drop_duplicates('Book-Title')
    return popular_books

@app.route("/")
def loginPage():
    return render_template('loginPage.html')

@app.route('/trending')
def trendingPage():
    # popular_books = find_popular_books()
    popular_books = pd.read_csv('Popular-Books.csv')
    # popular_books = popular_books.head(50)
    return render_template('trendingPage.html',
    Book_Name = list(popular_books['Book-Title']),
    Book_Author = list(popular_books['Book-Author']),
    Year_Publish = list(popular_books['Year-Of-Publication']),
    Publisher = list(popular_books['Publisher']),
    Image_S = list(popular_books['Image-URL-S']),
    Image_M = list(popular_books['Image-URL-M']),
    Image_L = list(popular_books['Image-URL-L'])
    )




def recommend(Book_Name):
    book_rating = pd.read_csv('Book-Rating.csv')
    x = book_rating.groupby('User-ID').count()['Book-Rating']>200
    Educated_users = x[x].index
    filtered_rating = book_rating[book_rating['User-ID'].isin(Educated_users)]  
    y = filtered_rating.groupby('Book-Title').count()['Book-Rating']>=50
    famous_books = y[y].index
    final = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
    pt = final.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
    pt.fillna(0,inplace=True)
    similarity_score = cosine_similarity(pt)
    book = pd.read_csv('Books.csv')
    index = np.where(pt.index==Book_Name)[0][0]
    distances = sorted(list(enumerate(similarity_score[index])),key=lambda i:i[1],reverse=True)[:15]
    x = []
    for i in distances:
        x.append(i[0])

    suggest = []
    for i in x:
        print(pt.index[i])
        suggest.append(pt.index[i])
    bn,ba,yp,p,il = [],[],[],[],[]
    for i in suggest:
        x = book[book['Book-Title'] == i]
        x = x.drop_duplicates('Book-Title')
        bn.extend(list(x['Book-Title'].values))
        ba.extend(list(x['Book-Author'].values))
        yp.extend(list(x['Year-Of-Publication'].values))
        p.extend(list(x['Publisher'].values))
        il.extend(list(x['Image-URL-L'].values))

        


    return [bn,ba,yp,p,il]


@app.route('/suggest',methods=['GET','POST'])
def suggestionPage():
    print(request.method)
    print(request.form)
    if request.method == 'POST':
        Book_Name = request.form['Book-Name']
        book_list = recommend(Book_Name)
        return render_template('suggestionPage.html',
    Book_Name = book_list[0],
    Book_Author = book_list[1],
    Year_Publish = book_list[2],
    Publisher = book_list[3],
    Image_L = book_list[4]
    )


    return render_template('suggestionPage.html')

@app.route('/choose')
def choose_book():
    popular_books = pd.read_csv('Good-Books.csv')


    # popular_books = popular_books.head(20)

    return render_template('chooseBook.html',
    Book_Name = list(popular_books['Book-Title']),
    Book_Author = list(popular_books['Book-Author']),
    Year_Publish = list(popular_books['Year-Of-Publication']),
    Publisher = list(popular_books['Publisher']),
    Image_S = list(popular_books['Image-URL-S']),
    Image_M = list(popular_books['Image-URL-M']),
    Image_L = list(popular_books['Image-URL-L'])
    )

if __name__ == '__main__':
    app.run(debug = True)
    # find_popular_books()

