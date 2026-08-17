from django.shortcuts import render, redirect
from products.models import Product
from products.views import delete_product
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm, EditForm
from .models import BaseUser, Buyer, Seller, Admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from main.functions import count_average


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        type = request.POST.get("type")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        if password != password_again:
            return render(request, "users/register.html", {"form": form, "message": "Пароли не совпадают"})
        if BaseUser.objects.filter(email=email):
            return render(request, "users/register.html", {"form": form, "message": "Указанная почта занята"})
        if not 14 < int(age) < 200:
            return render(request, "users/register.html", {"form": form, "message": "Недопустимый возраст"})
        BaseUser.objects.create_user(name, surname, type, email, password, gender, age)
        login(request, BaseUser.objects.get(email=email))
        return redirect("/")
    return render(request, "users/register.html", {"form": form})


def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = BaseUser.objects.get(email=email)
        if user:
            if user.get_user().check_password(password):
                login(request, user)
                return redirect("/")
        return render(request, "users/login.html", {"message": "Неправильный логин или пароль", "form": form})
    return render(request, "users/login.html", {"form": form})


@login_required(login_url="/account/login")
def account(request):
    rating = 0.0
    if request.user.type == "seller":
        all_products = Product.objects.filter(seller_id=request.user.id)
        if len(all_products) != 0:
            rating = count_average(all_products)
    return render(request, "users/account.html", {"rating": rating})


@login_required(login_url="/account/login")
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/account/login")
def delete_user(request):
    if request.user.type == "seller":
        all_products = Product.objects.filter(seller_id=request.user.id)
        for i in all_products:
            delete_product(i.id)
    user = request.user.get_user()
    request.user.delete()
    user.delete()
    return redirect("/")


@login_required(login_url="/account/login")
def edit_user(request):
    user = request.user.get_user()
    form = EditForm(
        {
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "gender": user.gender,
            "age": user.age,
            "password": "*",
            "password_again": "*"
        })
    if request.method == "POST":
        if request.POST.get("password") != request.POST.get("password_again"):
            return render(request, "users/edit.html", {"form": form, "message": "Пароли не совпадают"})
        if len(BaseUser.objects.filter(email=request.POST.get("email"))) > 1:
            return render(request, "users/edit.html", {"form": form, "message": "Указанная почта занята"})
        if not 14 < int(request.POST.get("age")) < 200:
            return render(request, "users/edit.html", {"form": form, "message": "Недопустимый возраст"})
        user = request.user.get_user()
        user.name = request.POST.get("name")
        user.surname = request.POST.get("surname")
        user.email = request.POST.get("email")
        user.set_password(request.POST.get("password"))
        user.gender = request.POST.get("gender")
        user.age = request.POST.get("age")
        user.save()
        user = request.user
        user.email = request.POST.get("email")
        user.save()
        return redirect("/account")
    return render(request, "users/edit.html", {"form": form})


def admin(request):
    return render(request, "users/admin.html")


def list_of_buyers(request):
    buyers = Buyer.objects.all()
    return render(request, "users/list_of_buyers.html", {"buyers": buyers})


def list_of_sellers(request):
    sellers = Seller.objects.all()
    return render(request, "users/list_of_sellers.html", {"sellers": sellers})


def list_of_admins(request):
    admins = Admin.objects.all()
    return render(request, "users/list_of_admins.html", {"admins": admins})


def delete_account_for_admin(request, id):
    user = BaseUser.objects.get(id=id)
    type = user.type
    if user.type == "seller":
        all_products = Product.objects.filter(seller_id=id)
        for i in all_products:
            delete_product(i.id)
    user_ = user.get_user()
    user_.delete()
    user.delete()
    return redirect(f"/account/admin/list_of_{type}s")


def give_admin(request, id):
    user = BaseUser.objects.get(id=id)
    user_ = user.get_user()
    id = user_.id
    name = user_.name
    surname = user_.surname
    email = user_.email
    password = user_.password
    gender = user_.gender
    age = user_.age
    date = user_.date
    user_.delete()
    admin = Admin()
    admin.id = id
    admin.name = name
    admin.surname = surname
    admin.email = email
    admin.set_password(password)
    admin.gender = gender
    admin.age = age
    admin.date = date
    admin.save()
    user.type = "admin"
    admin.save()
    return redirect("/account/admin/list_of_admins")


def give_buyer(request, id):
    user = BaseUser.objects.get(id=id)
    user_ = user.get_user()
    id = user_.id
    name = user_.name
    surname = user_.surname
    email = user_.email
    password = user_.password
    gender = user_.gender
    age = user_.age
    date = user_.date
    user_.delete()
    buyer = Buyer()
    buyer.id = id
    buyer.name = name
    buyer.surname = surname
    buyer.email = email
    buyer.set_password(password)
    buyer.gender = gender
    buyer.age = age
    buyer.date = date
    buyer.save()
    user.type = "buyer"
    user.save()
    return redirect("/account/admin/list_of_admins")
