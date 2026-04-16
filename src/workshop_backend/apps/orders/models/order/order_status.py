from django.db import models

class OrderStatus(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"