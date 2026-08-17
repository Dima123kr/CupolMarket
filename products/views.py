from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review
from basket.models import Basket
from users.models import Seller, Buyer
from .forms import ProductForm
from main.functions import new_product
from main.views import get_photos_from_id
import shutil
import os
from PIL import Image
from CupolMarket.settings import BASE_DIR
from main.functions import new_review, count_average


@login_required(login_url="/account/login")
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    try:
        shutil.rmtree(f"./static/photos/products/{product_id}")
    except Exception as err:
        pass

    reviews = Review.objects.filter(product_id=product_id)
    for i in reviews:
        try:
            shutil.rmtree(f"./static/photos/reviews/{i.id}")
        except Exception as err:
            pass
        i.delete()

    basket = Basket.objects.filter(product_id=product_id)
    for i in basket:
        i.delete()
    return redirect('/account')


@login_required(login_url="/account/login")
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(
        {
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "description": product.description
        })
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.quantity = request.POST.get("quantity")
        product.description = request.POST.get("description")
        product.save()
        return redirect(f'/product/add/{product_id}')
    return render(request, 'products/add_product.html', {"form": form})


@login_required(login_url="/account/login")
def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        product = new_product(
            request.user.id,
            request.POST.get("name"),
            request.POST.get("description"),
            request.POST.get("price"),
            request.POST.get("quantity")
        )
        return redirect(f"/product/add/{product.id}")
    return render(request, "products/add_product.html", {"form": form})


@login_required(login_url="/account/login")
def add_product_photo(request, product_id):
    try:
        photos = get_photos_from_id(product_id, "products")
    except Exception as err:
        photos = []
    if request.method == "GET":
        if "value" in request.GET:
            active = int(request.GET["value"])
            try:
                os.remove(str(BASE_DIR) + "/main" + get_photos_from_id(product_id, "products")[active])
            except Exception as err:
                pass
            return redirect(f"/product/add/{product_id}", code=200)
    if request.method == "POST":
        if "add_product" in request.POST:
            if len(get_photos_from_id(product_id, "products")) > 0:
                return redirect("/")
            else:
                return render(request, "products/add_product_photo.html",
                              {
                                  "photos": photos,
                                  "len_": len(photos),
                                  "product_id": product_id,
                                  "message": "Необходимо добавить как минимум одно фото"
                              })
        elif "add_photo" in request.POST:
            try:
                os.mkdir(str(BASE_DIR) + f"/main/static/photos/products/{product_id}")
            except Exception as err:
                pass
            f = request.FILES["photo"]
            if f:
                s = f.name
                Image.open(f).save(os.path.join(str(BASE_DIR) + f"/main/static/photos/products/{product_id}", s))
    try:
        photos = get_photos_from_id(product_id, "products")
    except Exception as err:
        photos = []
    return render(request, "products/add_product_photo.html",
                  {
                      "photos": photos,
                      "len_": len(photos),
                      "product_id": product_id
                  })


def product(request, product_id):
    reviews = Review.objects.filter(product_id=product_id)
    product = Product.objects.get(id=product_id)
    seller = Seller.objects.get(id=product.seller_id)
    reviews_info = []
    for i in reviews:
        try:
            user = (f"{Buyer.objects.get(id=i.buyer_id).name} "
                    f"{Buyer.objects.get(id=i.buyer_id).surname}")
        except Exception as err:
            user = "DELETED"
        reviews_info.append(
            {
                "username": user,
                "rating": i.rating,
                "text": i.text,
                "photos": get_photos_from_id(i.id, "reviews")
             })
    return render(request, "products/product.html",
                  {
                      "reviews": reviews_info,
                      "product": {
                          "id": product_id,
                          "name": product.name,
                          "seller": seller,
                          "description": product.description,
                          "price": product.price,
                          "rating": product.rating,
                          "quantity": product.quantity,
                          "photos": get_photos_from_id(product_id, "products")
                      }
                  })


@login_required(login_url="/account/login")
def add_review(request, product_id):
    products = Product.objects.all()
    products_ids = [int(i.id) for i in products]
    buyers = Buyer.objects.all()
    buyers_ids = [int(i.id) for i in buyers]
    return render(request, "products/add_review.html", {
        "is_not_buyer": request.user.id not in buyers_ids,
        "products_not_exists": product_id not in products_ids,
        "product_id": product_id
    })


@login_required
def submit_review(request, product_id):
    buyers = Buyer.objects.all()
    buyers_ids = [i.id for i in buyers]
    rating = request.POST.get("rating")
    review_text = request.POST.get("review")
    photo = request.FILES.get("photos")
    if request.user.id not in buyers_ids:
        return render(request, "products/add_review.html", {
            "is_not_buyer": request.user.id not in buyers_ids,
            "product_id": product_id
        })

    review = new_review(product_id, request.user.id, int(rating), review_text)
    try:
        os.mkdir(str(BASE_DIR) + f"/main/static/photos/reviews/{review.id}")
    except Exception as err:
        pass
    Image.open(photo).save(os.path.join(str(BASE_DIR) + f"/main/static/photos/reviews/{review.id}", f"{photo}.png"))
    average_reviews = count_average(Review.objects.filter(product_id=product_id))
    db_product = Product.objects.get(id=product_id)
    db_product.rating = average_reviews
    return redirect("/")
