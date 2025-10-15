from django.db import models

class MachineType(models.Model):
    type_name = models.CharField(max_length=40, blank=False, unique=True)

    def __str__(self):
        return f"{self.type_name}"


class Mark(models.Model):
    name = models.CharField(
        verbose_name="Марка", max_length=20, blank=False, unique=True
    )

    def __str__(self):
        return f"{self.name}"


class OrderStatus(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Job(models.Model):
    name = models.CharField(max_length=40, blank=False)
    repairman = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING)
    order = models.ForeignKey(
        "orders.Order", related_name="jobs", on_delete=models.DO_NOTHING
    )
    # parts = models.ManyToManyField(Part, blank=True)
    price = models.PositiveIntegerField(verbose_name="Цена(рубли)")
    warranty = models.PositiveIntegerField(verbose_name="Гарантия(дни)")
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}({self.repairman.last_name})"


class Settlement(models.Model):
    # Населённый пункт. Названия городов могут повторяться
    name = models.CharField(max_length=30, blank=False)
    type = models.CharField(
        max_length=30, choices=[("пос.", "посёлок"), ("гор.", "город")]
    )  # Дополнить

    def __str__(self):
        return f"{self.type} {self.name}"


class Street(models.Model):  # Надо ли привязывать улицу к городу??
    name = models.CharField(max_length=30)
    city = models.ForeignKey("orders.Settlement", on_delete=models.DO_NOTHING)
    prefix = models.CharField(
        max_length=15,
        choices=[("пер.", "переулок"), ("ул.", "улица"), ("пр.", "проспект")],
    )  # Дополнить choises

    def __str__(self):
        return f"{self.prefix} {self.name}"


class Machine(models.Model):
    type = models.ForeignKey("orders.MachineType", on_delete=models.DO_NOTHING)
    mark = models.ForeignKey("orders.Mark", on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=20, null=True, blank=True)
    serial_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.type} {self.mark} {self.model} {self.serial_number}"


class Order(models.Model):
    # Идентификатор в итоге должен состоять из даты и порядкового номера: 202509121
    machine = models.ForeignKey("orders.Machine", on_delete=models.DO_NOTHING)
    problem = models.CharField(max_length=100)
    # Как пометить, что заявка гарантийная?
    varranty_of = models.ForeignKey(
        "orders.Order", blank=True, null=True, on_delete=models.DO_NOTHING
    )
    status = models.ForeignKey("orders.OrderStatus", on_delete=models.DO_NOTHING)
    date_incomming = models.DateField(auto_now=True)  # Когда диспетчер принял заявку
    # Когда мастер начал работать
    date_begin = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    complekt = models.CharField(max_length=30, blank=True, null=True)
    additional = models.CharField(max_length=100, null=True, blank=True)
    repairman = models.ForeignKey(
        "auth.User", on_delete=models.DO_NOTHING, related_name="repairman_orders"
    )
    client = models.ForeignKey(
        "auth.User", on_delete=models.DO_NOTHING, related_name="client_order"
    )
    dispatcher = models.ForeignKey(
        "auth.User", related_name="despatcher_orders", on_delete=models.DO_NOTHING
    )  # Тот кто принял заявку
    inhouse = models.BooleanField(default=True)
    settlement = models.ForeignKey("orders.Settlement", on_delete=models.DO_NOTHING)
    street = models.ForeignKey(
        "orders.Street", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    building = models.CharField(max_length=10)  # Номер строения
    appartment = models.CharField(max_length=5, blank=True, null=True)  # Номер квартиры
    # Номер офиса, если есть
    office = models.CharField(max_length=5, blank=True, null=True)
    # photos = models.FileField(blank=True, null=True)#ну, допустим, шильдик аппарата

    def __str__(self):
        return f"Заказ №{self.pk}"

    class Meta:
        pass
        # permissions = []


class ServiceCallType(models.Model):
    """Таблица будет хранить типы заявок: забрать, доставить и прочее"""

    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"


class ServiceCall(models.Model):
    """Записи вызовов мастера на дом"""

    order = models.ForeignKey(
        "orders.Order", related_name="servicecalls", on_delete=models.DO_NOTHING
    )
    visit_datetime = models.DateTimeField()
    type = models.ForeignKey("orders.ServiceCallType", on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=20, null=True, blank=True)
    repairman = models.ForeignKey(
        "auth.User", related_name="repairman_servicecall", on_delete=models.DO_NOTHING
    )
    dispatcher = models.ForeignKey(
        "auth.User", related_name="dispatcher_servicecalls", on_delete=models.DO_NOTHING
    )  # Тот кто поставил заявку

    def __str__(self):
        return f"Тип:{self.type}; {self.order.machine}; Мастер: {self.repairman}; Диспетчер: {self.dispatcher}; Дата: {self.visit_datetime}"
