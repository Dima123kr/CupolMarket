from django.db.models import Model, IntegerField


class Basket(Model):
    product_id = IntegerField("ID товара, который был добавлен в корзину")
    buyer_id = IntegerField("ID покупателя, у которого данный товар находится в корзине")
    quantity = IntegerField("Количество товара, которое было добавлено в корзину")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Корзина"
