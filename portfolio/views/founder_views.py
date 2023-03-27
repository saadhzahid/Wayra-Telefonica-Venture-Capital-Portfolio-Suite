from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from portfolio.forms.founder_form import FounderForm
from portfolio.models.founder_model import Founder

"""
Create a founder.
"""


@login_required
def founder_create(request):
    if request.method == 'POST':
        founder_form = FounderForm(request.POST, prefix="form1")
        if founder_form.is_valid():
            founder_form.save()
            return redirect("individual_page")
    else:
        founder_form = FounderForm(prefix="form1")
    context = {
        'founderForm': founder_form
    }
    return render(request, "individual/founder_create.html", context=context)


"""
Delete a founder.
"""


@login_required
def founder_delete(request, id):
    founderInstance = Founder.objects.get(id=id)
    if request.method == 'POST':
        founderInstance.delete()
        return redirect('individual_page')
    return render(request, 'individual/founder_delete.html')


"""
Modify a founder.
"""


@login_required
def founder_modify(request, id):
    founder_form = Founder.objects.get(id=id)
    if request.method == 'POST':
        form1 = FounderForm(request.POST, instance=founder_form, prefix="form1")
        if form1.is_valid():
            form1.save()
            return redirect("individual_page")
    else:
        form1 = FounderForm(instance=founder_form, prefix="form1")
    context = {
        'founderForm': form1,
    }
    return render(request, 'individual/founder_modify.html', context=context)
