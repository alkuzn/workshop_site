from django.db import models

class Settlement(models.Model):
    # Населённый пункт. Названия городов могут повторяться
    name = models.CharField(max_length=30, blank=False)
    type = models.CharField(
        max_length=30, choices=[("пос.", "посёлок"), ("гор.", "город")]
    )  # Дополнить

    def __str__(self):
        return f"{self.type} {self.name}"