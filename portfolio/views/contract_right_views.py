from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DeleteView

from portfolio.forms import ContractRightForm
from portfolio.models.investment_model import ContractRight, Investment
from vcpms import settings


class ContractRightsListView(LoginRequiredMixin, ListView):
    template_name = 'investment/contract_rights/contract_right_list.html'
    paginate_by = settings.ITEM_ON_PAGE
    context_object_name = 'contract_rights'
    http_method_names = ['get']

    def dispatch(self, request, investment_id, *args, **kwargs):
        try:
            self.investment = Investment.objects.get(id=investment_id)
            return super().dispatch(request, investment_id, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('dashboard')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_id'] = self.investment.id
        if self.investment.investor.company:
            context['company_id'] = self.investment.investor.company.id
        if self.investment.investor.individual:
            context['individual_id'] = self.investment.investor.individual.id
        return context

    def get_queryset(self):
        return ContractRight.objects.filter(investment_id=self.investment.id).order_by('id')


class ContractRightCreateView(LoginRequiredMixin, CreateView):
    template_name = 'investment/contract_rights/contract_right_create.html'
    model = ContractRight
    pk_url_kwarg = 'id'
    # form_class = InvestmentForm # Temporary placeholder
    form_class = ContractRightForm
    http_method_names = ['get', 'post']

    def dispatch(self, request, investment_id, *args, **kwargs):
        self.investment_id = investment_id
        return super().dispatch(request, investment_id, *args, **kwargs)

    def form_valid(self, form):
        form.saveInvestment(Investment.objects.get(id=self.investment_id))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('contract_right_list', kwargs={'investment_id': self.investment_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_id'] = self.investment_id
        return context


class ContractRightDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'investment/contract_rights/contract_right_delete.html'
    http_method_names = ['get', 'post']
    model = ContractRight
    pk_url_kwarg = 'id'

    def dispatch(self, request, id, *args, **kwargs):
        try:
            right = ContractRight.objects.get(id=id)
            self.investment = right.investment
        except ObjectDoesNotExist:
            return redirect('dashboard')
        return super().dispatch(request, id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_id'] = self.investment.id
        return context

    def get_success_url(self):
        return reverse('contract_right_list', kwargs={'investment_id': self.investment.id})
