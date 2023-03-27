from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from portfolio.models import Company, Individual, Portfolio_Company, InvestorCompany, Founder, Investor

"""Archive views"""


@login_required
def archive(request):
    """This is the archive page. ONLY VIEWED BY ADMINS"""
    if request.user.is_staff:
        company_page_number = request.GET.get('page1', 1)
        individual_page_number = request.GET.get('page2', 1)

        companies = Company.objects.filter(is_archived=True).order_by('id')
        individuals = Individual.objects.filter(is_archived=True).order_by('id')

        companies_paginator = Paginator(companies, 5)
        individuals_paginator = Paginator(individuals, 5)

        try:
            companies_page = companies_paginator.page(company_page_number)
            individuals_page = individuals_paginator.page(individual_page_number)

        except EmptyPage:
            companies_page = []
            individuals_page = []

        context = {
            "companies": companies_page,
            "individuals": individuals_page,
            "search_url": reverse('archive_search'),
            "placeholder": "Search through the archive"
        }

        return render(request, 'archive/archive_page.html', context)
    else:
        return redirect('logout')


@login_required
def archive_search(request):
    if request.user.is_staff:
        if request.method == "GET":

            searched = request.GET['searchresult']

            response = []

            if searched == "":
                response = []
            else:
                if request.session['archived_company_filter'] == '3':
                    investor_companies = InvestorCompany.objects.all()
                    company_search_result = Company.objects.filter(id__in=investor_companies.values('company'),
                                                                   name__contains=searched,
                                                                   is_archived=True).values().order_by('id')
                elif request.session['archived_company_filter'] == '2':
                    company_search_result = Portfolio_Company.objects.filter(parent_company__name__contains=searched,
                                                                             is_archived=True).values().order_by('id')
                else:
                    company_search_result = Company.objects.filter(name__contains=searched,
                                                                   is_archived=True).values().order_by('id')

                if request.session['archived_individual_filter'] == '2':
                    founder_individuals = Founder.objects.all()
                    individual_search_result = Individual.objects.filter(
                        id__in=founder_individuals.values('individualFounder'), name__contains=searched,
                        is_archived=True).values().order_by('id')
                elif request.session['archived_individual_filter'] == '3':
                    individual_search_result = Investor.objects.filter(individual__name__contains=searched,
                                                                       is_archived=True).values().order_by(
                        'id')
                else:
                    individual_search_result = Individual.objects.filter(name__contains=searched,
                                                                         is_archived=True).values().order_by('id')
                response.append(
                    ("Companies", list(company_search_result[:4]), {'destination_url': 'portfolio_company'}))
                response.append(
                    ("Individuals", list(individual_search_result[:4]), {'destination_url': 'individual_profile'}))

            search_results_table_html = render_to_string('partials/search/search_results_table.html', {
                'search_results': response, 'searched': searched, "destination_url": "portfolio_company"})

            return HttpResponse(search_results_table_html)

        else:
            return HttpResponse("Request method is not a GET")
    else:
        return redirect('logout')


@login_required
def change_archived_company_filter(request):
    if request.user.is_staff:
        if request.method == "GET":
            filter_number = request.GET['filter_number']
            page_number = request.GET.get('page1', 1)
            if filter_number:
                request.session['archived_company_filter'] = filter_number
            else:
                request.session['archived_company_filter'] = 1

            if request.session['archived_company_filter'] == '3':
                investor_companies = InvestorCompany.objects.all()
                result = Company.objects.filter(id__in=investor_companies.values('company'), is_archived=True).order_by(
                    'id')
            elif request.session['archived_company_filter'] == '2':
                result = Portfolio_Company.objects.filter(parent_company__is_archived=True).order_by('id')
            else:
                result = Company.objects.filter(is_archived=True).order_by('id')

            paginator = Paginator(result, 6)

            try:
                companies_page = paginator.page(page_number)
            except EmptyPage:
                companies_page = []

            context = {
                "companies": companies_page,
            }

            archived_companies_table_html = render_to_string('archive/archived_companies_table.html', context, request)

            return HttpResponse(archived_companies_table_html)
    else:
        return redirect('logout')


@login_required
def change_archived_individual_filter(request):
    if request.user.is_staff:
        if request.method == "GET":
            filter_number = request.GET['filter_number']
            page_number = request.GET.get('page2', 1)
            if filter_number:
                request.session['archived_individual_filter'] = filter_number
            else:
                request.session['archived_individual_filter'] = 1

            if request.session['archived_individual_filter'] == '2':
                founder_individuals = Founder.objects.all()
                result = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'),
                                                   is_archived=True).order_by('id')
            elif request.session['archived_individual_filter'] == '3':
                all_investors = Investor.objects.all()
                result = Individual.objects.filter(id__in=all_investors.values('individual'),
                                                   is_archived=True).order_by('id')
            else:
                result = Individual.objects.filter(is_archived=True).values().order_by('id')

            paginator = Paginator(result, 6)

            try:
                individuals_page = paginator.page(page_number)
            except EmptyPage:
                individuals_page = []

            context = {
                "individuals": individuals_page,
            }

            archived_individuals_table_html = render_to_string('archive/archived_individuals_table.html', context,
                                                               request)

            return HttpResponse(archived_individuals_table_html)
    else:
        return redirect('logout')
