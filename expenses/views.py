from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense, Image, UploadFile,DocumentUpload
from .forms import DocumentForm,MyModelForm,DocumentUploadForm
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences


# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    images = Image.objects.filter(owner=request.user)
    documents = DocumentUpload.objects.filter(owner=request.user)
    print(images)
    if UserPreferences.objects.filter(user=request.user).exists():
        currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = 'NGN-Nigerian Naira'
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'images': images,
        'documents': documents

    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':

        return render(request, 'expenses/add_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        Expense.objects.create(owner=request.user,
                               amount=amount, description=description, date=date, category=category)
        messages.success(request, 'Expense was saved successfully')
        return redirect('expenses')


def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':

        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__startswith=search_str, owner=request.user) | Expense.objects.filter(date__startswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


def add_image(request):
    if request.method == 'POST':
        image = request.POST['image']
        name = request.POST['name']
        # print(request.POST['image'])
        if not image:
            print('no image')
            messages.error(request, "image is required")
            return render(request, 'expenses/add_expense.html', )
        Image.objects.create(owner=request.user,
                             document=image, name=name)
        messages.success(request, "your image has been uploaded")
        return redirect('expenses')

    if request.method == 'GET':

        return render(request, 'expenses/add_expense.html', )


def upload_file(request):
        if request.method == 'POST':
            print(request.POST, request.FILES)
            # form = DocumentForm(request.POST, request.FILES)
            form = DocumentUploadForm(request.POST, request.FILES)

            context = {'form': form}
            print(form.is_valid())
            print(form.errors)
            if form.is_valid():
                document_upload = form.save(commit=False)
                document_upload.owner = request.user
                document_upload.save()
                messages.success(request,'Your file has been save')
                return redirect('expenses')
            messages.error(request, form.errors)
            return render(request, 'expenses/upload_files.html', context)

        else:
            # form = DocumentForm()
            form = DocumentUploadForm()

        context = {'form': form, }
        return render(request, 'expenses/upload_files.html', context)


def upload_document(request):

    if request.method == 'POST':
        file = request.FILES.get("file")
        title = request.POST.get("title")
        context = {
            'file': file,
            'title': title,
        }
        print(context)
        if not file:
            messages.error(request, "file is required")
            return render(request, 'expenses/upload_files.html', context)
        if not title:
            messages.error(request, "title is required")
            return render(request, 'expenses/upload_files.html', context)

        UploadFile.objects.create(title=title, file=file)
        messages.success(request, "your image has been uploaded")
        return redirect('expenses')

    else:
        context = {'values': request.POST, }
    return render(request, 'expenses/upload_files.html', context)


def upload_view(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = MyModelForm()

    return render(request, 'upload_form.html', {'form': form})