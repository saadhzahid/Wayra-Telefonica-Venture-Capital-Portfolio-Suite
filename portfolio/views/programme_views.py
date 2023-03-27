from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView, ListView

from portfolio.forms import CreateProgrammeForm, EditProgrammeForm
from portfolio.models import Programme, Document
from vcpms import settings


class SearchProgramme(TemplateView):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        searched = request.GET['searchresult']
        search_result = {}
        if searched != "":
            search_result = Programme.objects.filter(name__contains=searched).values()

        search_results_table_html = render_to_string('programmes/search/search_results_table.html', {
            'search_results': list(search_result), 'searched': searched})

        return HttpResponse(search_results_table_html)

    def post(self, request, *args, **kwargs):
        page_number = request.POST.get('page', 1)
        searched = request.POST['searchresult']
        if searched == "":
            return redirect('programme_list')

        programmes = Programme.objects.filter(name__contains=searched).values().order_by('id')

        paginator = Paginator(programmes, 6)
        try:
            programmes_page = paginator.page(page_number)
        except EmptyPage:
            programmes_page = []

        return render(request, 'programmes/programme_list_page.html',
                      {"programmes": programmes_page, "searched": searched})


class ProgrammeListView(LoginRequiredMixin, ListView):
    template_name = 'programmes/programme_list_page.html'
    context_object_name = 'programmes'
    paginate_by = settings.ITEM_ON_PAGE

    def get_queryset(self):
        return Programme.objects.all().order_by('id')


class ProgrammeCreateView(LoginRequiredMixin, CreateView):
    model = Programme
    form_class = CreateProgrammeForm
    template_name = 'programmes/programme_create_page.html'

    def get_success_url(self):
        return reverse('programme_list')


class ProgrammeUpdateView(LoginRequiredMixin, UpdateView):
    model = Programme
    form_class = EditProgrammeForm
    http_method_names = ['get', 'post']
    template_name = 'programmes/programme_update_page.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.get_object().id
        return context

    def get_initial(self):
        return model_to_dict(self.get_object())


class ProgrammeDeleteView(LoginRequiredMixin, DeleteView):
    model = Programme
    template_name = 'programmes/programme_delete_page.html'
    http_method_names = ['get', 'post']
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('programme_list')


class ProgrammeDetailView(LoginRequiredMixin, DetailView):
    model = Programme
    template_name = 'programmes/programme_page.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context['id'] = instance.id
        context['partners'] = instance.partners.all()
        context['participants'] = instance.participants.all()
        context['coaches_mentors'] = instance.coaches_mentors.all()
        context['documents'] = Document.objects.filter(programme=instance)
        return context
