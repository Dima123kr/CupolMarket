from django.db.models import Model, EmailField, CharField, IntegerField, DateTimeField, FloatField, BooleanField
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, surname, type, email, password, gender, age, is_boss=False):
        user = BaseUser(
            email=email,
            type=type
        )
        user.save(using=self._db)
        if type == "buyer":
            buyer = Buyer(
                id=user.id,
                name=name,
                surname=surname,
                email=email,
                gender=gender,
                age=age
            )
            buyer.set_password(password)
            buyer.save(using=self._db)
        elif type == "seller":
            seller = Seller(
                id=user.id,
                name=name,
                surname=surname,
                email=email,
                gender=gender,
                age=age
            )
            seller.set_password(password)
            seller.save(using=self._db)
        elif type == "admin":
            admin = Admin(
                id=user.id,
                name=name,
                surname=surname,
                email=email,
                gender=gender,
                age=age,
                is_boss=is_boss
            )
            admin.set_password(password)
            admin.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser, PermissionsMixin):
    use_in_migrations = True

    password = None
    last_login = None
    is_superuser = None

    email = EmailField("Почтовый адрес", unique=True)
    type = CharField("Тип пользователя", max_length=30)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["type"]

    def get_user(self):
        return eval(self.type.capitalize()).objects.get(id=self.id)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Buyer(Model):
    name = CharField("Имя", max_length=30)
    surname = CharField("Фамилия", max_length=30)
    email = EmailField("Почтовый адрес")
    password = CharField("Пароль", max_length=30)
    gender = CharField("Пол", max_length=30)
    age = IntegerField("Возраст")
    date = DateTimeField("Дата и время создания аккаунта", default=datetime.datetime.now)

    def __str__(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Seller(Model):
    name = CharField("Имя", max_length=30)
    surname = CharField("Фамилия", max_length=30)
    email = EmailField("Почтовый адрес")
    password = CharField("Пароль", max_length=30)
    gender = CharField("Пол", max_length=30)
    age = IntegerField("Возраст")
    rating = FloatField("Рейтинг", default=0.0)
    date = DateTimeField("Дата и время создания аккаунта", default=datetime.datetime.now)

    def __str__(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"


class Admin(Model):
    name = CharField("Имя", max_length=30)
    surname = CharField("Фамилия", max_length=30)
    email = EmailField("Почтовый адрес")
    password = CharField("Пароль", max_length=30)
    gender = CharField("Пол", max_length=30)
    age = IntegerField("Возраст")
    is_boss = BooleanField("Является ли администратор главным?", default=False)
    date = DateTimeField("Дата и время создания аккаунта", default=datetime.datetime.now)

    def __str__(self):
        return self.email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"
