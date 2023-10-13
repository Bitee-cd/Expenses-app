from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Source
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences


# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    if UserPreferences.objects.filter(user=request.user).exists():
        currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = 'NGN-Nigerian Naira'
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':

        return render(request, 'income/add_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        Income.objects.create(owner=request.user,
                              amount=amount, description=description, date=date, source=source)
        messages.success(request, 'Income was saved successfully')
        return redirect('income')


def income_edit(request, id):
    sources = Source.objects.all()
    income = Income.objects.get(pk=id)
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':

        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit-income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit-income.html', context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.source = source
        income.save()
        messages.success(request, 'Income updated successfully')
        return redirect('income')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed')
    return redirect('income')


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        income = Income.objects.filter(amount__startswith=search_str, owner=request.user) | Income.objects.filter(date__startswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(source__icontains=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)
