from django.shortcuts import render
from django.http import JsonResponse
from basket.models import Basket
from main.views import get_photos_from_id
from products.models import Product
from users.models import Seller, Buyer
from main.functions import new_basket


def get(request):
    basket_data = {
        "items": [],
        "total": 0
    }
    products = Basket.objects.filter(buyer_id=request.user.id)
    for i in products:
        prd = Product.objects.get(id=i.product_id)
        bask_str = Basket.objects.get(product_id=i.product_id, buyer_id=request.user.id)
        basket_data["items"].append({
            "image": get_photos_from_id(i.product_id, "products")[0],
            "name": prd.name,
            "price": prd.price,
            "quantity": bask_str.quantity
        })
    basket_data["total"] = sum([int(i["price"]) * int(i["quantity"]) for i in basket_data["items"]])
    return JsonResponse(basket_data, safe=False)


def payment(request):
    print(1)
    products = Basket.objects.filter(buyer_id=request.user.id)
    for i in products:
        product = Product.objects.get(id=i.product_id)
        product.quantity -= i.quantity
    for i in products:
        i.delete()
    return JsonResponse({}, safe=False)


def add(request, product_id):
    try:
        data = Basket.objects.all()
        if request.user.type != "buyer":
            return JsonResponse({"success": "0"}, safe=False)
        users_ids = [i.buyer_id for i in data]
        products_ids = [i.product_id if i.buyer_id == request.user.id else None for i in data]
        product_to_by = Product.objects.get(id=product_id)
        if int(request.user.id) in users_ids and int(product_id) in products_ids:
            db_basket_product = Basket.objects.get(product_id=product_id, buyer_id=request.user.id)
            if db_basket_product.quantity == product_to_by.quantity:
                return JsonResponse({"success": "3"}, safe=False)
            db_basket_product.quantity = min(db_basket_product.quantity + 1, product_to_by.quantity)
        else:
            if product_to_by.quantity == 0:
                return JsonResponse({"success": "2"}, safe=False)
            new_basket(request.user.id, product_id, 1)
        return JsonResponse({"success": "1"}, safe=False)
    except Exception as ex:
        print(ex)
        return JsonResponse({"success": False}, safe=False)


def basket(request):
    buyers_ids = Buyer.objects.all()
    buyers_ids = [buyer.id for buyer in buyers_ids]
    if request.user.id not in buyers_ids:
        return render(request, "products/add_review.html", {"is_not_buyer": True})
    return render(request, "basket/basket.html")
