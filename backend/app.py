from flask import Flask, request, jsonify, Response
from config import Config
from models import *
from datetime import datetime, timedelta
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from tools import workers, task
from flask_mail import Mail
from io import StringIO
import csv
from flask_caching import Cache



app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
db.init_app(app)
cache = Cache(app)
ma.init_app(app)
bcrypt.init_app(app)

mail = Mail(app)

celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND']
)
celery.Task = workers.ContextTask
app.app_context().push()

def CreateAdmin():
    if User.query.filter_by(role ='admin').first() is None:
        new_user = User(email='admin@gmail.com', name='Admin', password='1234', role='admin', last_loggedin=datetime.now())
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
    return "Admin Created"

with app.app_context():
    db.create_all()
    CreateAdmin()

CORS(app, supports_credentials=True)

@app.route("/")
def home():
    return "Library Management Application"



@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    name = data["name"]
    password = data["password"]
    role = data["role"]
    last_loggedin = datetime.now()

    if not email or not name or not password or not role:
        return {"error": "All fields are required"}, 400
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "User already exists"}, 409
    
    new_user = User(email=email, name=name, password=password, role=role, last_loggedin=last_loggedin)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create user"}, 500

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    if not email or not password:
        return {"error": "All fields are required"}, 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"error": "Invalid email or password"}, 401
    
    user.last_loggedin = datetime.now()
    db.session.commit()

    access_token = create_access_token(identity={
        "email": user.email,
        "role": user.role
    })

    return jsonify({"access_token": access_token, "message": "Login successful"}), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(current_user)
    return "You are the lucky one!, " + current_user["email"] + "!", 200

@app.route('/getuserinfo', methods=['GET'])
@jwt_required()
def getuserinfo():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user["email"]).first()
    user_data = user_schema.dump(user)
    return jsonify(user_data), 200
    
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'logout successful'})
    unset_jwt_cookies(response)
    return response

# CRUD ON CATEGORIES
# CREATE
@app.route('/add-section', methods=['POST'])
@jwt_required()
def create_section():
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    data = request.json
    name = data["name"]
    if not name:
        return {"error": "Name is required"}, 400
    existing_section = Section.query.filter_by(name=name).first()
    if existing_section:
        return {"error": "Section already exists"}, 409
    verified = True if (this_user["role"] == 'admin')  else False
    new_section = Section(name=name, creator_email=this_user["email"], verified=verified)
    try:
        db.session.add(new_section)
        db.session.commit()
        if verified:
            return {"message": "Section created successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create section"}, 500

# READ ALL sections
@app.route('/sections', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    sections_data = sections_schema.dump(sections)
    return jsonify(sections_data), 200


# READ ONE section
@app.route('/section/<int:id>', methods=['GET'])
def get_section(id):
    section = Section.query.filter_by(id=id).first()
    if not section:
        return {"error": "Section not found"}, 404
    section_data = section_schema.dump(section)
    return jsonify(section_data), 200

# UPDATE section
@app.route('/section/<int:id>', methods=['PUT'])
@jwt_required()
def update_section(id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    data = request.json
    name = data["name"]
    if not name:
        return {"error": "Name is required"}, 400
    section = Section.query.filter_by(id=id).first()
    if not section:
        return {"error": "Section not found"}, 404
    existing_section = Section.query.filter_by(name=name).first()
    if existing_section and existing_section.id != section.id:
        return {"error": "Section already exists"}, 409
    section.name = name
    try:
        db.session.commit()
        return {"message": "Section updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to update section"}, 500

# DELETE CATEGORIES
@app.route('/section/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    this_user = get_jwt_identity()
    if this_user["role"] != "admin":
        return {"error": "Unauthorized"}, 401
    section = Section.query.filter_by(id=id).first()
    if not section:
        return {"error": "Section not found"}, 404
    try:
        db.session.delete(section)
        db.session.commit()
        return {"message": "Section deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete section"}, 500


@app.route('/section/<int:section_id>/add-book', methods=['POST'])
@jwt_required()
def add_book(section_id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": 'Page Restricted!'}, 401
    
    data = request.json
    print(data)
    
    title = data.get('title')
    author = data.get('author')
    price = data.get('price')
    content = data.get('content')

    if not title or not author or not price or not content:
        return {"error": "Required Fields Missing"}, 400
    if price <= 0:
        return {"error": "Quantity must be greater than 0"}, 400
    section = Section.query.filter_by(id=section_id).first()
    if not section:
        return {"error": "Section not found"}, 404
    new_book = Book(title = title,
                          author=author,
                          price=price,
                          content=content,
                          section_id=section_id,
                          date_added=datetime.now())
    try:
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book added successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to add a book"}, 500

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_data = books_schema.dump(books)
    return jsonify(books_data), 200

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return {"error": "book not found"}, 404
    book_data = book_schema.dump(book)
    return jsonify(book_data), 200

@app.route('/update-book/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    try:
        this_user = get_jwt_identity()
        if this_user["role"] == "user":
             return {"error": "Unauthorized"}, 401

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.price = data.get('price', book.price)
        book.content = data.get('content', book.content)

        db.session.commit()

        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        print(f"Error occurred while updating book: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500




@app.route('/deletebook/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    this_user = get_jwt_identity()
    if this_user["role"] == "user":
        return {"error": "Unauthorized"}, 401
    book = Book.query.filter_by(id=id).first()
    if not book:
        return {"error": "Product not found"}, 404
    try:
        db.session.delete(book)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to delete product"}, 500


@app.route("/add-to-cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    this_user = get_jwt_identity()
    if this_user["role"] != "user":
        return {"error": "Unauthorized"}, 401

    data = request.json
    book_id = data["book_id"]
    
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return {"error": "book not found"}, 404
    
    user_cart = BookCart.query.filter_by(user_email=this_user["email"]).first()
   
 
    if not user_cart:
        user_cart = BookCart(user_email=this_user["email"])
        try:
            db.session.add(user_cart)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to create cart"}, 500
    cart_items = CartItems.query.filter_by(bookcart_id=user_cart.id).all()
    cart_items_data = []
    for item in cart_items:
        if item.status == 0 or item.date_return > datetime.now():
            cart_items_data.append(item)
    if len(cart_items_data)==3:
         return {"error": "Sorry, you can issue maximum 3 books"}, 500
    cart_item = CartItems.query.filter_by(bookcart_id=user_cart.id, book_id=book_id).first()
    if cart_item:
        return {"message": "Book already requested"}, 201
    else:
        cart_item = CartItems(bookcart_id = user_cart.id, book_id = book_id)
    try:
        db.session.add(cart_item)
        db.session.commit()
        return {"message": "Book added to cart successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to add book to cart"}, 500


@app.route('/view-cart', methods=['GET'])
@jwt_required()
def view_cart():
    this_user = get_jwt_identity()
    user_cart = BookCart.query.filter_by(user_email=this_user["email"]).first()
    if not user_cart:
        return {"msg": "Cart is empty"}, 200
    cart_items = CartItems.query.filter_by(bookcart_id=user_cart.id).all()
    cart_items_data = []
    for item in cart_items:
        if item.status == 0:
            cart_items_data.append({
                'cart_id': item.id,
                'book_id': item.book_id,
                'book_name':item.book.title,
                'author':item.book.author,
                'price':item.book.price
            })
    return jsonify({"cart":cart_items_data}), 200



@app.route("/delete-from-cart/<int:cart_item_id>", methods=["DELETE"])
@jwt_required()
def delete_from_cart(cart_item_id):
    current_user = get_jwt_identity()
    # if current_user["role"] != "user":
    #     return {"error": "Unauthorized"}, 401

    cart_item = CartItems.query.filter_by(id=cart_item_id).first()
    if not cart_item:
        return {"error": "Cart item not found"}, 404
    
    user_cart = BookCart.query.filter_by(id=cart_item.bookcart_id, user_email=current_user["email"]).first()
    if not user_cart:
        return {"error": "Unauthorized to delete this cart item"}, 401
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Cart item deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete cart item: {str(e)}"}, 500



@app.route("/getallbookinfo", methods=['GET'])
def getallbookinfo():
    sections = Section.query.all()
    data = []
    for section in sections:
        data.append({
            'id': section.id,
            'name': section.name,
            'books': books_schema.dump(section.books)
        })
    return jsonify(data), 200


@app.route('/book-requests', methods=['GET'])
@jwt_required()
def book_requests():
    current_user = get_jwt_identity()
    if current_user["role"] == "user":
        return {"error": 'Page Restricted!'}, 401
    cart_items = CartItems.query.all()
    cart_items_data = []
    for item in cart_items:
        cart_item = BookCart.query.get(item.bookcart_id)
        cart_items_data.append({
                'cart_id': item.id,
                'user': cart_item.user_email,
                'book_id': item.book_id,
                'book_name':item.book.title,
                'date_issued':item.date_issued,
                'status':item.status,
                'date_return':item.date_return
            })
    return jsonify({"cart":cart_items_data}), 200



@app.route("/admin-approve/<int:cart_item_id>")
@jwt_required()
def adminapprove(cart_item_id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return {"error": "Unauthorized"}, 401
    cart_item = CartItems.query.filter_by(id=cart_item_id).first()
    cart_item.status = 1
    # CartItems('cart_id','book_id','book_name','price').query.filter_by(cart_id=cart_item.id).update(dict(status = 1))
    cart_item.date_issued = datetime.now()
    cart_item.date_return = datetime.now() + timedelta(minutes=10)
    try:
        db.session.commit()
        task.send_bookissued_email.delay(cart_item.id)
        return {"message": "Book approved successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error":"Failed to approve the requests"}, 500

@app.route("/delete-from-bookrequests/<int:cart_item_id>", methods=["DELETE"])
@jwt_required()
def delete_from_bookrequests(cart_item_id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return {"error": "Unauthorized"}, 401

    cart_item = CartItems.query.filter_by(id=cart_item_id).first()
    if not cart_item:
        return {"error": "Cart item not found"}, 404
    
    # user_cart = BookCart.query.filter_by(id=cart_item.bookcart_id, user_email=current_user["email"]).first()
    # if not user_cart:
    #     return {"error": "Unauthorized to delete this cart item"}, 401
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        return {"message": "Cart item deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete cart item: {str(e)}"}, 500   


    
@app.route('/user-book', methods=['GET'])
@jwt_required()
def user_book():
    this_user = get_jwt_identity()
    user_cart = BookCart.query.filter_by(user_email=this_user["email"]).first()
    if not user_cart:
        return {"msg": "Cart is empty"}, 200
    cart_items = CartItems.query.filter_by(bookcart_id=user_cart.id).all()
    cart_items_data = []
    for item in cart_items:
        if item.status == 1 and item.date_return > datetime.now():
            cart_items_data.append({
                'cart_id': item.id,
                'book_id': item.book_id,
                'book_name':item.book.title,
                'author':item.book.author,
                'date_issued':item.date_issued,
                'date_return':item.date_return,
                'content':item.book.content
            })
    return jsonify({"cart":cart_items_data}), 200


@app.route('/read-book/<int:book_id>', methods=['GET'])
def read_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        book_data = book_schema.dump(book)
        section = Section.query.get(book.section_id)
        return jsonify({'book':book_data, "section_name": section.name}), 200
    except Exception as e:
        print(f"Error occured while getting book: {str(e)}")
        return jsonify({'message': 'Oops, Somthing went wrong!'}), 500

def generate_bookissued_csv():
    issued_books = CartItems.query.all()

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['ID', 'Book title', 'Issued Date', 'Return Date'])
    for book in issued_books:
        book1 = BookCart.query.get(book.bookcart_id)
        if book.date_issued is not None:
            csv_writer.writerow([book1.user_email, book.book.title, book.date_issued.strftime('%Y-%m-%d'), book.date_return.strftime('%Y-%m-%d')])

    return csv_buffer.getvalue()

@app.route('/download-bookissue-csv', methods=['GET'])
@cache.cached(timeout=10)
def download_order_csv():
    csv_data = generate_bookissued_csv()
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=bookissue.csv'})




if __name__ == "__main__":
    app.run(debug=True)

