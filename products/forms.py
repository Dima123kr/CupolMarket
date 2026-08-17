from django.forms import Form, CharField, IntegerField, DecimalField, TextInput,Textarea


class ProductForm(Form):
    name = CharField(max_length=30, widget=TextInput(attrs={"placeholder": "Название товара", "class": "form-control"}))
    price = DecimalField(widget=TextInput(attrs={"placeholder": "Цена", "class": "form-control"}),
                         decimal_places=2, min_value=0.01)
    quantity = IntegerField(widget=TextInput(attrs={"placeholder": "Количество на складе", "class": "form-control"}),
                            min_value=0)
    description = CharField(widget=Textarea(attrs={"placeholder": "Описание товара", "class": "form-control"}))
