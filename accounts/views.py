from curses.ascii import HT
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from django.utils.translation import activate
activate('az')

from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from .models import Account

@require_http_methods(["GET", "POST"])
def signin(request):

    if request.user.is_authenticated:
        return redirect('base:index')

    if request.method == 'POST':

        form = LoginForm(request.POST)
       
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            if user is not None:
                
                login(request, user)
                
                user.last_login = datetime.datetime.now()
                user.save()

                if request.GET.get('next', None):
                    return redirect(request.GET.get('next', None))

                return redirect('base:index')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'login_form':form})
    

@require_http_methods(["GET", "POST"])
@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
    return render(request, 'accounts/logout.html')


# ACCOUNT

@require_http_methods(["GET", "POST"])
@login_required
@permission_required('accounts.view_account', raise_exception=True)
def index(request):

    accounts = Account.objects.filter(is_superuser=False)

    return render(request, 'accounts/list.html', context={
        'accounts':accounts,
    })


@require_http_methods(["GET", "POST"])
@login_required
@permission_required('accounts.add_account', raise_exception=True)
def create(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save()

            staffGroup = Group.objects.get(name='staff')
            user.groups.set([staffGroup])

            messages.success(request, 'İşçi əlavə edildi!')
            return redirect('accounts:create')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/create.html', context={'form':form})


@require_http_methods(["GET", "POST"])
@login_required
@permission_required('accounts.change_account', raise_exception=True)
def edit(request, id):

    account = get_object_or_404(Account, id = id)
   
    if request.POST:
        form = ProfileUpdateForm(request.POST, instance = account)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(request, 'İşçinin məlumatları yeniləndi!')
            return redirect('accounts:edit', id=id)

    else:
        form = ProfileUpdateForm(initial={
            "email":account.email,
            "username":account.username,
            'first_name':account.first_name,
            'last_name':account.last_name,
        })

    return render(request, 'accounts/edit.html', context={
        'form':form, 'account':account
    })


@require_http_methods(["POST"])
@login_required
@permission_required('accounts.delete_account', raise_exception=True)
def delete(request, id):

    account = get_object_or_404(Account, id = id)
    account.delete()
    messages.success(request, 'İşçi silindi!')
    return redirect("accounts:list")


