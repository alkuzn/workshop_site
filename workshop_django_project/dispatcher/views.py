from django.shortcuts import render
from django.forms.models import inlineformset_factory

from dispatcher.forms import CreateOrderForm,EditOrderForm,MachineForm
from orders.models import Order, Machine
#удалить заявку можно только если по ней не начата работа или вообще нельзя?
def dispatcher_view(request):
    formc = CreateOrderForm(
        instance=Order.objects.first()
    )
    #machineform = MachineForm(instance=Machine.objects.first())
    machineform = MachineForm()
    #formset = inlineformset_factory()
    return render(request, "dispatcher_main_page.html", context={"create_form": formc, 
                                                                 "edit_form": EditOrderForm(prefix="edit"),
                                                                 "machineform": machineform
                                                                 })

def repairman_view(request):
    
    return render(request, "repairman.html")