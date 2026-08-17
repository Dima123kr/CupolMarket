from django.forms import Form, CharField, ChoiceField, PasswordInput, IntegerField, EmailField, EmailInput
from django.forms import TextInput, RadioSelect


class RegisterForm(Form):
    type = ChoiceField(label="Зарегистрироваться как:", choices=[("buyer", "Покупатель"), ("seller", "Продавец")],
                       widget=RadioSelect(attrs={"label": "Зарегистрироваться как:"}))
    name = CharField(max_length=30, widget=TextInput(attrs={"placeholder": "Имя", "class": "form-control"}))
    surname = CharField(max_length=30, widget=TextInput(attrs={"placeholder": "Фамилия", "class": "form-control"}))
    email = EmailField(widget=EmailInput(attrs={"placeholder": "Почтовый адрес", "class": "form-control"}))
    password = CharField(max_length=50, widget=PasswordInput(attrs={"placeholder": "Пароль", "class": "form-control"}))
    password_again = CharField(max_length=50,
                               widget=PasswordInput(attrs={"placeholder": "Повторите пароль", "class": "form-control"}))
    gender = ChoiceField(label="Пол:", choices=[("male", "Мужской"), ("female", "Женский")],
                         widget=RadioSelect(attrs={"label": "Пол:"}))
    age = IntegerField(widget=TextInput(attrs={"placeholder": "Возраст", "class": "form-control"}))


class LoginForm(Form):
    email = EmailField(widget=EmailInput(attrs={"placeholder": "Почтовый адрес", "class": "form-control"}))
    password = CharField(max_length=50, widget=PasswordInput(attrs={"placeholder": "Пароль", "class": "form-control"}))


class EditForm(Form):
    name = CharField(max_length=30, widget=TextInput(attrs={"placeholder": "Имя", "class": "form-control"}))
    surname = CharField(max_length=30, widget=TextInput(attrs={"placeholder": "Фамилия", "class": "form-control"}))
    email = EmailField(widget=EmailInput(attrs={"placeholder": "Почтовый адрес", "class": "form-control"}))
    password = CharField(max_length=50, widget=PasswordInput(attrs={"placeholder": "Пароль", "class": "form-control"}))
    password_again = CharField(max_length=50,
                               widget=PasswordInput(attrs={"placeholder": "Повторите пароль", "class": "form-control"}))
    gender = ChoiceField(label="Пол:", choices=[("male", "Мужской"), ("female", "Женский")],
                         widget=RadioSelect(attrs={"label": "Пол:"}))
    age = IntegerField(widget=TextInput(attrs={"placeholder": "Возраст", "class": "form-control"}))
