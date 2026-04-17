from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Dish 

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('_username')
        password = request.POST.get('_password')

        try:
            account = Account.objects.get(username=username, password=password)
            request.session['user_id'] = account.id
            return redirect('basic_list', pk=account.id)
        except Account.DoesNotExist:
            return render(request, 'tapasapp/login_page.html', {'error': 'Invalid login'})
    
    success = request.GET.get('success')
    return render(request, 'tapasapp/login_page.html', {'success': success})
    
def basic_list(request, pk):
    if 'user_id' not in request.session or request.session['user_id'] != pk:
        return redirect('login_page')
    user = get_object_or_404(Account, pk=pk)
    dishes = Dish.objects.all()
    return render(request, 'tapasapp/basic_list.html', {'dishes': dishes, 'user_obj': user})

def manage_account(request, pk):
    user=get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/manage_account.html', {'user_obj': user})
                                                   
def change_password(request, pk):
    user=get_object_or_404(Account, pk=pk)
    error = None

    if request.method == 'POST': 
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password != user.password:
            error = "Current password is incorrect"
        elif new_password != confirm_password:
            error = "New passwords do not match"
        else:
            user.password = new_password
            user.save()
            return redirect('manage_account', pk=pk)
    
    return render(request, 'tapasapp/change_password.html', {'user_obj': user, 'error': error})

def signup_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password:
            error = "Username and password are required"
        elif Account.objects.filter(username=username).exists():
            error = "Username already exists"
        elif password != confirm_password:
            error = "Passwords do not match"
        else:
            Account.objects.create(username=username, password=password)
            return redirect('/?success=Account created successfully')
        
    return render(request, 'tapasapp/signup.html', {'error': error})

def delete_account(request, pk):
    user=get_object_or_404(Account, pk=pk)

    if request.method == 'POST': 
        user.delete()
        if 'user_id' in request.session:
            del request.session['user_id']
        return redirect('login_page')
    
    return render(request, 'tapasapp/delete_account.html', {'user_obj': user})

def logout_view(request): 
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login_page')

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        user_id = request.session.get('user_id')
        return redirect('basic_list', pk=user_id)
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    user_id = request.session.get('user_id')
    return redirect('basic_list', pk=user_id)

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/update_menu.html', {'d':d})