from django import forms
from django.forms import BaseForm, ModelForm

from orders.models import Order, Machine
from orders.serializers import NewOrderSerializer

class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = "__all__"

class CreateOrderForm(ModelForm):
    #machine = MachineForm()
    #date_visit = forms.DateTimeField()
    class Meta:
        model = Order
        fields = "__all__"
        exclude = NewOrderSerializer.Meta.exclude

class EditOrderForm(ModelForm):
    id = forms.HiddenInput()
    status = forms.CharField(disabled=True)
    dispatcher = forms.CharField(disabled=True)
    date_incomming = forms.CharField(disabled=True)
    date_begin = forms.CharField(disabled=True)
    date_end = forms.CharField(disabled=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["date_end", 'machine']