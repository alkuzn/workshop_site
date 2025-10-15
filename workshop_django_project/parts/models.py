from django.db import models

# Create your models here.
class Part(models.Model):
    name = models.CharField(max_length=10)
    #count = models.IntegerField()
    #price = models.DecimalField()#За штуку
    #partnumber = models.CharField(max_length=10)

class PartRequest(object):
    employee = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    part = models.ForeignKey("Part", on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    #photos

class PartArrivals(object):
    part = models.ForeignKey(Part, on_delete=models.DO_NOTHING)#Какую запчасть купили
    custom_label = models.CharField(max_length=20)#Чтобы не заносить в список
    count = models.PositiveIntegerField()#Сколько купили
    date = models.DateField()#Когда пришла
    buyer = models.ForeignKey("User", on_delete=models.DO_NOTHING)#Кто купил