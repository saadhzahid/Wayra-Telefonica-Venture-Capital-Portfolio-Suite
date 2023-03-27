from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from portfolio.forms import InvestmentForm, InvestorCompanyCreateForm, InvestorEditForm, PortfolioCompanyCreateForm, \
    PortfolioCompanyEditForm
from portfolio.models import Investment, Portfolio_Company
from portfolio.models.investor_model import Investor


class InvestmentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'investment/investment_create.html'
    model = Investment
    form_class = InvestmentForm
    http_method_names = ['get', 'post']

    def dispatch(self, request, company_id, *args, **kwargs):
        self.company_id = company_id
        return super().dispatch(request, company_id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        return context

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})


class InvestmentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'investment/investment_update.html'
    model = Investment
    form_class = InvestmentForm
    pk_url_kwarg = 'id'
    http_method_names = ['get', 'post']

    def dispatch(self, request, id, *args, **kwargs):
        self.investment_id = id
        self.company_id = Investment.objects.get(id=id).investor.id
        return super().dispatch(request, id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        context['investment_id'] = self.investment_id
        return context

    def get_initial(self):
        return model_to_dict(self.get_object())

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})


class InvestmentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'investment/investment_delete.html'
    model = Investment
    pk_url_kwarg = 'id'
    http_method_names = ['get', 'post']

    def dispatch(self, request, id, *args, **kwargs):
        self.investment_id = id
        self.company_id = Investment.objects.get(id=id).investor.id
        return super().dispatch(request, id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        context['investment_id'] = self.investment_id
        return context

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})


class InvestorCompanyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'investment/investor_company_create.html'
    model = Investor
    form_class = InvestorCompanyCreateForm
    http_method_names = ['get', 'post']

    def form_valid(self, form):
        self.redirect_id = form.cleaned_data['company'].id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.redirect_id})


class InvestorCompanyUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'investment/investor_company_update.html'
    model = Investor
    form_class = InvestorEditForm
    http_method_names = ['get', 'post']
    pk_url_kwarg = 'company_id'

    def dispatch(self, request, company_id, *args, **kwargs):
        self.company_id = company_id
        return super().dispatch(request, company_id, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        return context

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})


class PortfolioCompanyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'investment/portfolio_company_create.html'
    model = Portfolio_Company
    form_class = PortfolioCompanyCreateForm
    http_method_names = ['get', 'post']

    def form_valid(self, form):
        self.redirect_id = form.cleaned_data['parent_company'].id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.redirect_id})


class PortfolioCompanyUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'investment/portfolio_company_update.html'
    model = Portfolio_Company
    form_class = PortfolioCompanyEditForm
    http_method_names = ['get', 'post']
    pk_url_kwarg = 'company_id'

    def dispatch(self, request, company_id, *args, **kwargs):
        self.company_id = company_id
        return super().dispatch(request, company_id, *args, **kwargs)

    def get_object(self, queryset=None):
        return Portfolio_Company.objects.get(parent_company_id=self.company_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_id'] = self.company_id
        return context

    def get_success_url(self):
        return reverse('portfolio_company', kwargs={'company_id': self.company_id})
