from products.models import Product, Review
from basket.models import Basket
from .models import Emails
import os
from CupolMarket.settings import BASE_DIR


def new_product(seller_id, name, description, price, quantity):
    product = Product()
    product.seller_id = seller_id
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity
    product.save()
    return product


def new_basket(buyer_id, product_id, quantity):
    basket = Basket()
    basket.buyer_id = buyer_id
    basket.product_id = product_id
    basket.quantity = quantity
    basket.save()
    return basket


def new_review(product_id, buyer_id, rating, text):
    review = Review()
    review.product_id = product_id
    review.buyer_id = buyer_id
    review.rating = rating
    review.text = text
    review.save()
    return review


def new_email(email_):
    email = Emails()
    email.email = email_
    email.save()
    return email


def count_average(query):
    summary = 0
    counter = 0
    for i in query:
        summary += i.rating
        counter += 1
    return round(summary / counter, 2)


def get_photos_from_id(id, mode):
    try:
        path = str(BASE_DIR).replace("\\", "/")
        arr = os.listdir(path + f'/main/static/photos/{mode}/{id}')
        arr = list(map(lambda x: f'/static/photos/{mode}/{id}/{x}', arr))
        return arr
    except Exception as ex:
        return []
