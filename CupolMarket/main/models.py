from django.db.models import Model, EmailField


class Emails(Model):
    email = EmailField("Почтовый адрес")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Почтовый адрес"
        verbose_name_plural = "Почтовые адреса"
