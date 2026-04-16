from django.db import models

#Никому кроме диспетчера не нужны списки машин
class Machine(models.Model):
    type = models.ForeignKey("orders.MachineType", on_delete=models.DO_NOTHING)
    mark = models.ForeignKey("orders.Brand", null=True, default=1, on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=20, null=True, blank=True)
    serial_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.type} {self.mark} {self.model} {self.serial_number}"