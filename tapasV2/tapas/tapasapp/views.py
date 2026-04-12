from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Account, Dish 

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('_username')
        password = request.POST.get('_password')
        a = Account.objects.filter(username=username, password=password)
        return render(request, 'basic_list.html') 
    else:
        return redirect('no_login')
    
def no_login(request):
    success = request.session.pop('signup_success', None)

    if request.method == 'POST':
        return render(request, 'login_page.html', {'success': success})
    else:
        return redirect('login_page', {'success': success})

def manage_account(request, pk):
    user=get_object_or_404(Account, pk=pk)
    return render(request, 'manage_account.html', {'user_obj': user})
                                                   
def change_password(request, pk):
    user=get_object_or_404(Account, pk=pk)
    error = None

    if request.method == 'POST': 
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password != user.password:
            error = "Current password is incorrect"
            return render(request, 'change_password.html', {
                'user_obj': user,
                'error': error
                })
        if new_password != confirm_password:
            error = "New passwords do not match"
            return render(request, 'change_password.html', {
                'user_obj': user,
                'error': error
            })
        
        user.password = new_password
        user.save()

        return redirect('manage_account', pk=pk)
    
    return render(request, 'change_password.html', {'user_obj': user, 'error': error})

def signup_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if Account.objects.filter(username=username).exists():
            error = "Account already exists"
            return render(request, 'signup.html', {'error': error})
        
        # if password is matching obv
        if password != confirm_password:
            error = "Passwords do not match"
            return render(request, 'signup.html', {'error': error})
        
        if not username or not password:
            error = "Username and password are required"
            return render(request, 'signup.html', {'error': error})
        
        Account.objects.create(username=username,password=password)

        return redirect('/?success=Account created successfully')
        
    return render(request, 'signup.html', {'error': error})

def delete_account(request, pk):
    user=get_object_or_404(Account, pk=pk)

    if request.method == 'POST': 
        user.delete()
        logout(request)
        return redirect('login')
    
    return render(request, 'delete_account.html', {'user_obj': user})

def logout_view(request): 
    logout(request)
    return redirect('login')

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})