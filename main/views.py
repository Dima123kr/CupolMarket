from django.shortcuts import render
from products.models import Product
from django.http import JsonResponse
from .functions import new_email, get_photos_from_id
from difflib import SequenceMatcher
from users.models import BaseUser


def main(request):
    return render(request, "main/main.html")


def load_more(request):
    products = Product.objects.all()
    start = int(request.GET["start"])
    limit = int(request.GET["limit"])
    new_products = products[start:start + limit]
    data = []
    for i in new_products:
        data.append({"id": i.id, "name": i.name, "image": get_photos_from_id(i.id, "products")[0], "price": i.price,
                     "rating": i.rating})
    return JsonResponse(data, safe=False)


def load_more_search(request):
    query = str(request.GET["query"])
    start = int(request.GET["start"])
    limit = int(request.GET["limit"])
    print(query, start, limit)
    products = Product.objects.all()
    products = list(filter(lambda x: SequenceMatcher(None, x.name, query).ratio() >= 0.7, products))
    new_products = products[start:start + limit]
    data = []
    for i in new_products:
        data.append({"id": i.id, "name": i.name, "image": get_photos_from_id(i.id, "products")[0], "price": i.price,
                     "rating": i.rating})
    return JsonResponse(data, safe=False)


def get_seller_products(request):
    products = []
    all_products = Product.objects.filter(seller_id=request.user.id)
    for el in all_products:
        product_data = {
            "id": el.id,
            "name": el.name,
            "price": el.price,
            "image": get_photos_from_id(el.id, "products")[0],
            "quantity": el.quantity,
            "rating": el.rating
        }
        products.append(product_data)
    return JsonResponse(products, safe=False)


def search_result(request, query):
    return render(request, "main/search.html")


def about_us(request):
    return render(request, "main/about_us.html")


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_email(email)
        return JsonResponse({"message": "Вы успешно подписались!"}, safe=False), 200
