from django.db import models

class Brand(models.Model):
    name = models.CharField(
        verbose_name="Марка", max_length=20, blank=False, unique=True
    )

    def __str__(self):
        return f"{self.name}"