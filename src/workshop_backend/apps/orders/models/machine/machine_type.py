from django.db import models

class MachineType(models.Model):
    type_name = models.CharField(max_length=40, blank=False, unique=True)

    def __str__(self):
        return f"{self.type_name}"