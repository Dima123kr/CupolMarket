from django.db.models import Model, IntegerField, CharField, TextField, FloatField, DateTimeField
import datetime


class Product(Model):
    seller_id = IntegerField("ID продавца")
    name = CharField("Название", max_length=100)
    description = TextField("Описание")
    price = FloatField("Цена")
    quantity = IntegerField("Количество на складе")
    rating = FloatField("Рейтинг", default=0.0)
    number_of_purchases = IntegerField("Количество проданных товаров", default=0)
    date = DateTimeField("Дата и время добавления товара", default=datetime.datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Review(Model):
    product_id = IntegerField("ID товара, на который оставили отзыв")
    buyer_id = IntegerField("ID покупателя, оставившего отзыв")
    rating = IntegerField("Оценка")
    text = TextField("Текст")
    date = DateTimeField("Дата и время, когда был оставлен отзыв", default=datetime.datetime.now())

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
