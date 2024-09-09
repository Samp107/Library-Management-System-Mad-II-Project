from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"

    email = Column(Text, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    role = Column(Text, default='user', nullable=False) # "admin" or "user"
    last_loggedin = Column(DateTime, nullable=False)

    def __init__(self, email, name, password, role, last_loggedin):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.role = role
        self.last_loggedin = last_loggedin

class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "name", "password", "role", "last_loggedin")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Section(db.Model):
    __tablename__ = "section"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    books = relationship("Book", back_populates="section", cascade="all, delete-orphan")

    def __init__(self, name, creator_email, verified=False):
        self.name = name

class SectionSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)


class  Book(db.Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)
    section = relationship("Section", back_populates="books")
    date_added = Column(DateTime)
    bookcarts = relationship("CartItems", back_populates="book", cascade="all, delete-orphan")
    order = relationship("OrderItems", back_populates="book", cascade="all, delete-orphan")

    def __init__(self, title, author, price, content, section_id, date_added):
        self.title = title
        self.author = author
        self.price = price
        self.content = content
        self.section_id = section_id
        self.date_added = date_added

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "price", "content", "section_id", "date_added")

book_schema = BookSchema()
books_schema = BookSchema(many=True)


class BookCart(db.Model):
    __tablename__ = "book_cart"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(Text, ForeignKey("user.email"),nullable=False)
    user = relationship("User", backref="bookcart")
    items = relationship("CartItems", back_populates="bookcart", cascade="all, delete-orphan")


class CartItems(db.Model):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bookcart_id = Column(Integer, ForeignKey("book_cart.id"), nullable=False)
    bookcart = relationship("BookCart", back_populates="items")
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    book = relationship("Book", back_populates="bookcarts")
    status = Column(Integer, default=0, nullable=False)
    date_issued = Column(DateTime(), default=None)
    date_return = Column(DateTime(), default=None)
    


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(Text, ForeignKey("user.email"),nullable=False)
    user = relationship("User", backref="order")
    total_amount = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)
    items = relationship("OrderItems", back_populates="order", cascade = "all, delete-orphan")

class OrderItems(db.Model):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order", back_populates="items")
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    book = relationship("Book", back_populates="order")
    
