from .workers import celery
from models import *
from .mailer import send_email
from flask import render_template
from celery.schedules import crontab
from datetime import datetime, timedelta


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30, daily_reminder.s(), name="every day reminder (every minute)")
    # sender.add_periodic_task(30, daily_reminder.s(), name="every day reminder (every day at 10 AM)")
    sender.add_periodic_task(30, monthly_report.s(), name="monthly report (every min)")



@celery.task
def send_bookissued_email(id):
    cart_item = CartItems.query.get(id)
    book_cart = BookCart.query.get(cart_item.bookcart_id)
    book = Book.query.get(cart_item.book_id)
    user = User.query.get(book_cart.user_email)
    subject = "Book issued Successful"
    html = render_template('bookissue.html', cart_item = cart_item, book_cart = book_cart, book = book)
    send_email(book_cart.user_email, subject, html)
    return f"email successfully sent to {user.name}"


@celery.task
def daily_reminder():
    twenty_four_hours_ago = datetime.now() - timedelta(seconds=30)
    inactive_users = User.query.filter(User.last_loggedin < twenty_four_hours_ago).filter(User.role == "user").all()
    message = "You are getting this mail, because you haven't logged in for 24 hours. Please login again."
    for user in inactive_users:
        html = render_template('daily_reminder.html', user=user, message=message)
        send_email(user.email, "You are missing out a best books", html)
        
    return f"successfully sent email to {len(inactive_users)} users"

@celery.task
def monthly_report():
    users = User.query.filter_by(role="user").all()

    for user in users:
        one_month_ago = datetime.now() - timedelta(days=30)
        book_cart = BookCart.query.filter_by(user_email = user.email).first()
        if book_cart:
            user_issued_books = CartItems.query.filter_by(bookcart_id=book_cart.id).filter(CartItems.date_issued > one_month_ago).all()

        issued_books_details = []
    

        for item in user_issued_books:
            
            issued_books_details.append({
                'Book_name': item.book.title,
                'Issued_date': item.date_issued.strftime('%Y-%m-%d %H:%M'),
                'Return_date': item.date_return.strftime('%Y-%m-%d %H:%M'),
            })

        html = render_template('monthly_report.html', user=user, issued_books_details=issued_books_details)
        send_email(subject = "Monthly Report", to = user.email, html = html)

    return "success"


