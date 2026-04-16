from django.db import models

class Street(models.Model):  # Надо ли привязывать улицу к городу??
    name = models.CharField(max_length=30)
    city = models.ForeignKey("orders.Settlement", on_delete=models.DO_NOTHING)
    prefix = models.CharField(
        max_length=15,
        choices=[("пер.", "переулок"), ("ул.", "улица"), ("пр.", "проспект")],
    )  # Дополнить choises

    def __str__(self):
        return f"{self.prefix} {self.name}"