from django.db import models

class Order(models.Model):
    #Нужна таблица учета статусов заказа или перечислением?
    # Идентификатор в итоге должен состоять из даты и порядкового номера: 202509121 ?
    # Как пометить, что заявка гарантийная?Попробую статусами
    machine = models.ForeignKey("orders.Machine", on_delete=models.DO_NOTHING)
    problem = models.CharField(max_length=100)
    created = models.DateField(auto_now=True)  # Когда диспетчер принял заявку
    finished = models.DateTimeField(null=True)
    varranty_finished_date = models.DateTimeField(null=True)
    complekt = models.CharField(max_length=30, blank=True, null=True)
    creator = models.ForeignKey(
        "auth.User", related_name="created_orders", on_delete=models.DO_NOTHING
    )
    additional_contacts = models.JSONField(null=True)#типа {"сосед": '+70000000000', 'сестра': '+70000000000'}
    #area = models.ForeignKey("orders.Area", on_delete=models.DO_NOTHING)#Область
    settlement = models.ForeignKey("orders.Settlement", on_delete=models.DO_NOTHING)
    street = models.ForeignKey(
        "orders.Street", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    building = models.CharField(max_length=10)  # Номер строения
    client = models.ForeignKey(#Этого поля не должно быть в этой таблице?
        "auth.User", on_delete=models.DO_NOTHING, related_name="client_order"
    )
    appartment = models.CharField(max_length=5, blank=True, null=True)  # Номер квартиры, и номер офиса. Так попробую
    status = models.ForeignKey("orders.OrderStatus", on_delete=models.DO_NOTHING)
    #additional = models.CharField(max_length=100, null=True)#Будет отдельная таблица notes?
    #varranty_of = models.OneToOneField( #Гарантия должна быть только на работу а не тут
    #    "orders.Order", blank=True, null=True, on_delete=models.DO_NOTHING
    #)
    # Номер офиса, если есть
    #office = models.CharField(max_length=5, blank=True, null=True)
    #paid_date = models.DateField()#Устанавливается, когда все работы завершены и оплачены Этого в это таблице быть не должно
    #total_price //записываем конечную стоимость ремонта, когда все работы завершены
    

    def __str__(self):
        return f"Заказ №{self.pk}"

    class Meta:
        pass
        # permissions = []