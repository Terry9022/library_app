# app.py

from flask import Flask, render_template, request, flash, session, redirect, url_for
from sqlalchemy.sql import text
from models import db, User, Book, Author, Borrow
from datetime import datetime
from datetime import date
import csv 

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 3}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

db.init_app(app)

# Call the function to create tables when the application starts
# create_tables()
@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all()
        # Create some users
        user1 = User(name='John Doe', email='john@example.com', address='123 Main St')
        user2 = User(name='Jane Smith', email='jane@example.com', address='456 Park Ave')
        user3 = User(name='Bob Smith', email='bob@example.com', address='789 Elm St')
        user4 = User(name='Sara Lee', email='sara@example.com', address='321 Oak Rd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        user5 = User(name='Michael Johnson', email='michael@example.com', address='555 Forest Ave')
        user6 = User(name='Michelle Davis', email='michelle@example.com', address='633 Hill St') 
        user7 = User(name='David Lee', email='david@example.com', address='977 Mountain Rd')
        user8 = User(name='Jessica Miller', email='jessica@example.com', address='1122 Oak Ct')
        user9 = User(name='Chris Rodriguez', email='chris@example.com', address='234 Cherry Rd')
        db.session.add_all([user5, user6, user7, user8, user9])
        # Create some authors
        author1 = Author(name='J.K. Rowling', biography='Author of the Harry Potter series')  
        author2 = Author(name='Stephen King', biography='Prolific horror and suspense novelist')
        author3 = Author(name='J.R.R. Tolkien', biography='Author of Lord of the Rings') 
        author4 = Author(name='Agatha Christie', biography='Mystery writer known for detectives Poirot and Marple')
        db.session.add(author1)
        db.session.add(author2)
        db.session.add(author3)
        db.session.add(author4)
        author5 = Author(name='Charles Dickens', biography='Victorian era author known for novels like Oliver Twist')  
        author6 = Author(name='Jane Austen', biography='Regency era novelist known for Pride and Prejudice')
        author7 = Author(name='Mark Twain', biography='American author of novels like Huckleberry Finn')
        author8 = Author(name='William Shakespeare', biography='Iconic English playwright and poet')
        author9 = Author(name='Emily Dickinson', biography='Influential American poet')
        db.session.add_all([author5, author6, author7, author8, author9])
        # Create some books
        book1 = Book(title='Harry Potter and the Sorcerer\'s Stone', author=author1, genre='Fantasy', publish_date=datetime.strptime('1997-06-26', '%Y-%m-%d'))
        book2 = Book(title='It', author=author2, genre='Horror', publish_date=datetime.strptime('1986-09-15', '%Y-%m-%d'))
        book3 = Book(title='The Hobbit', author=author3, genre='Fantasy', publish_date=datetime.strptime('1937-09-21', '%Y-%m-%d'))
        book4 = Book(title='Murder on the Orient Express', author=author4, genre='Mystery', publish_date=datetime.strptime('1934-01-01', '%Y-%m-%d'))
        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)
        db.session.add(book4)
        book5 = Book(title='Great Expectations', author=author5, genre='Drama', publish_date= datetime.strptime('1861-01-01', '%Y-%m-%d'))
        book6 = Book(title='Pride and Prejudice', author=author6, genre='Romance', publish_date= datetime.strptime('1813-01-28', '%Y-%m-%d'))
        book7 = Book(title='The Adventures of Huckleberry Finn', author=author7, genre='Adventure', publish_date= datetime.strptime('1884-12-10', '%Y-%m-%d'))
        book8 = Book(title='Romeo and Juliet', author=author8, genre='Tragedy', publish_date= datetime.strptime('1597-01-01', '%Y-%m-%d')) 
        book9 = Book(title='Poems', author=author9, genre='Poetry', publish_date= datetime.strptime('1890-01-01', '%Y-%m-%d'))
        db.session.add_all([book5, book6, book7, book8, book9])
        # Create some borrows
        borrow1 = Borrow(user=user1, book=book1, checkout_date=datetime.strptime('2023-01-15', '%Y-%m-%d') , due_date=datetime.strptime('2024-01-29', '%Y-%m-%d') , return_date=None)
        borrow2 = Borrow(user=user2, book=book2, checkout_date=datetime.strptime('2023-01-20', '%Y-%m-%d')  , due_date=datetime.strptime('2023-02-03', '%Y-%m-%d') , return_date= datetime.strptime('2023-01-25', '%Y-%m-%d') )
        borrow3 = Borrow(user=user3, book=book3, checkout_date= datetime.strptime('2023-01-03', '%Y-%m-%d') , due_date= datetime.strptime('2023-01-17', '%Y-%m-%d'), return_date= datetime.strptime('2023-01-15', '%Y-%m-%d'))
        borrow4 = Borrow(user=user4, book=book4, checkout_date= datetime.strptime('2023-01-25', '%Y-%m-%d') , due_date=datetime.strptime('2024-02-08' , '%Y-%m-%d'), return_date=None) 
        db.session.add(borrow1)
        db.session.add(borrow2)
        db.session.add(borrow3)  
        db.session.add(borrow4)
        db.session.commit()
        flash('Create database tables successfully!',"alert-success")
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('show_users.html', users=users) 

@app.route('/books')
def show_books():
    books = Book.query.all()
    return render_template('show_books.html', books=books)

@app.route('/authors')
def show_authors():
    authors = Author.query.all()
    return render_template('show_authors.html', authors=authors)

@app.route('/borrows')
def show_borrows():
  borrows = Borrow.query.all()
  return render_template('show_borrows.html', borrows=borrows)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get(book_id)
    borrows = Borrow.query.filter_by(book_id=book.id).all()
    return render_template('book_detail.html', book=book, borrows=borrows)

@app.route('/user/<int:user_id>') 
def user_profile(user_id):
    user = User.query.get(user_id)
    borrows = Borrow.query.filter_by(user_id=user.id).all() 
    return render_template('user_profile.html', user=user, borrows=borrows)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_id = request.form['user_id']
        due_date = request.form['due_date']

        new_borrow = Borrow(user_id=user_id, 
                            book_id=book_id,
                            checkout_date= date.today(),
                            due_date=datetime.strptime(due_date, '%Y-%m-%d') 
                            )
        
        db.session.add(new_borrow)
        db.session.commit()

        flash('Book borrowed successfully!',"alert-success")
        return redirect(url_for('index'))

    return render_template('borrow_book.html',book=book)

@app.route('/return/<int:borrow_id>', methods=['GET', 'POST'])  
def return_book(borrow_id):

    borrow = Borrow.query.get(borrow_id)
    if request.method == 'POST':
        borrow_id = request.form['borrow_id']
        borrow = Borrow.query.get(borrow_id)
        
        borrow.return_date = datetime.today()
        
        db.session.commit()

        flash('Book returned successfully!',"alert-success")
        return redirect(url_for('index'))

    return render_template('return_book.html', borrow=borrow)

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):

    user = User.query.get(user_id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']

        db.session.commit()
        return redirect(url_for('user_profile', user_id=user.id))

    return render_template('edit_user.html', user=user)

@app.route('/sql', methods=['GET', 'POST'])
def sql_query():

  if request.method == 'POST':
    query = request.form['query']
    result = None
    
    try:
        result = db.session.execute(text(query)).fetchall()
    except Exception as e:
        print(e)
        flash('Error executing query: ' + str(e),'alert-danger')
        return redirect('/sql')

    return render_template('sql.html', query=query, result=result)

  return render_template('sql.html')

@app.route('/insert_more_books')
def insert_more_books():
    with app.app_context():
        with open('books_record.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip header row
            
            for row in csv_reader:
                author = Author(name= row[2])
                book = Book(title=row[1], author=author, genre=row[3], publish_date=datetime.strptime(row[4], '%d/%m/%y'))
                db.session.add(book)

            db.session.commit() 
            print("Added books from CSV!")
        flash('Insert more books into database successfully!',"alert-success")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
