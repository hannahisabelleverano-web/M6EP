from django.shortcuts import get_object_or_404, render, redirect
from .models import Supplier, WaterBottle, Account
from django.contrib.auth import logout 


# Create your views here.

def view_supplier(request):
    if 'user_id' not in request.session:
        return redirect('login_view')
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'suppliers': supplier_objects})


def view_bottles(request):
    if 'user_id' not in request.session:
        return redirect('login_view')
    bottle_objects = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottle_objects})

def view_bottle_details(request, pk):
    if 'user_id' not in request.session:
        return redirect('login_view')
    bottle_object = WaterBottle.objects.get(pk=pk)
    return render(request, 'MyInventoryApp/view_bottle_details.html', {'bottle': bottle_object})

def delete_bottle(request, pk):
    if 'user_id' not in request.session:
        return redirect('login_view')
    bottle_object = WaterBottle.objects.get(pk=pk)
    bottle_object.delete()
    return redirect('view_bottles')


def add_bottle(request):
    if 'user_id' not in request.session:
        return redirect('login_view')
    supplier_objects = Supplier.objects.all()

    if request.method == 'POST':
        sku = request.POST.get('sku')
        brand = request.POST.get('brand')
        cost = request.POST.get('cost')
        size = request.POST.get('size')
        mouth_size = request.POST.get('mouth_size')
        color = request.POST.get('color')
        supplied_by_id = request.POST.get('supplied_by')
        current_quantity = request.POST.get('current_quantity')

        supplier = get_object_or_404(Supplier, pk=supplied_by_id)

        WaterBottle.objects.create(
            sku=sku, 
            brand=brand, 
            cost=cost, 
            size=size, 
            mouth_size=mouth_size, 
            color=color, 
            supplied_by_id=supplier,
            current_quantity=current_quantity)
        return redirect('view_bottles')
    return render(request, 'MyInventoryApp/add_bottle.html', {'suppliers': supplier_objects})

def login_view(request): 
    error = None 
    success = request.GET.get('success', None)
    if request.method == 'POST': 
        username= request.POST.get('username')
        password= request.POST.get('password')

        existing_user= Account.objects.filter(username=username, password=password)

        if existing_user: 
            return redirect('view_bottles', pk=existing_user.first().pk)
        
        else: 
            error = "Invalid Login"

    return render(request, 'MyInventoryApp/login_view.html', {'error': error, 'success': success})

def signup_view(request): 
    error_in_signup = None
    if request.method == 'POST': 
        username= request.POST.get('username')
        password= request.POST.get('password')
    
        if Account.objects.filter(username=username).exists(): 
            error_in_signup = "Account already existing"
        
        else: 
            Account.objects.create(username=username, password=password)

    return render(request, 'MyInventoryApp/login_view.html', {'error': error_in_signup, 'success': 'Account created successfully'})

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login_view')

def manage_account(request, pk):
    if 'user_id' not in request.session or request.session['user_id'] != pk:
        return redirect('login_view')
    account_object = Account.objects.get(pk=pk)
    return render(request, 'MyInventoryApp/manage_account.html', {'account': account_object})

def change_password(request, pk):
    if 'user_id' not in request.session or request.session['user_id'] != pk:
        return redirect('login_view')
    
    user = get_object_or_404(Account, pk=pk)
    error = None

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password != user.password:
            error = "The current password is incorrect."
            return render(request, 'MyInventoryApp/change_password.html', {'account': user, 'error': error})
        
        if new_password != confirm_password:
            error = "The new passwords do not match"
            return render(request, 'MyInventoryApp/change_password.html', {'account': user, 'error': error})
        
        user.password = new_password
        user.save()
        return redirect('manage_account', pk=pk)
    return render(request, 'MyInventoryApp/change_password.html', {'account': user, 'error': error})

def delete_account(request, pk):
    if 'user_id' not in request.session or request.session['user_id'] != pk:
        return redirect('login_view')
    
    user = get_object_or_404(Account, pk=pk)
    user.delete()
    del request.session['user_id']
    return redirect('login_view')

def basic_list(request, pk):
    if 'user_id' not in request.session or request.session['user_id'] != pk:
        return redirect('login_view')
    user = get_object_or_404(Account, pk=pk)
    supplier_count = Supplier.objects.count()
    bottle_count = WaterBottle.objects.count()
    return render(request, 'MyInventoryApp/basic_list.html' , {'account': user, 'supplier_count': supplier_count, 'bottle_count': bottle_count})