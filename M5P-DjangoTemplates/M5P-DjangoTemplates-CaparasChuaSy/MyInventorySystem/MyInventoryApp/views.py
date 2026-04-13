from django.shortcuts import render, redirect
from .models import Supplier, WaterBottle, Account
from django.contrib.auth import logout 


# Create your views here.

def view_supplier(request):
    if 'user_id' not in request.session:
        return redirect('login_page')
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'suppliers': supplier_objects})


def view_bottles(request):
    if 'user_id' not in request.session:
        return redirect('login_page')
    bottle_objects = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottle_objects})

def view_bottle_details(request, pk):
    if 'user_id' not in request.session:
        return redirect('login_page')
    bottle_object = WaterBottle.objects.get(pk=pk)
    return render(request, 'MyInventoryApp/view_bottle_details.html', {'bottle': bottle_object})

def delete_bottle(request, pk):
    if 'user_id' not in request.session:
        return redirect('login_page')
    bottle_object = WaterBottle.objects.get(pk=pk)
    bottle_object.delete()
    return redirect('view_bottles')


def add_bottle(request):
    if 'user_id' not in request.session:
        return redirect('login_page')
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

        supplier = Supplier.objects.get(pk=supplied_by_id)

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
    if request.method == 'POST': 
        username= request.POST.get('username')
        password= request.POST.get('password')

        existing_user= Account.objects.filter(username=username, password=password)

        if existing_user: 
            return redirect('suppliers')
        
        else: 
            error = "Invalid Login"

    return render(request, 'login.html', {'error': error})

def signup_view(request): 
    error_in_signup = None
    if request.method == 'POST': 
        username= request.POST.get('username')
        password= request.POST.get('password')
    
        if Account.objects.filter(username=username).exists(): 
            ExistingUser="Account already existing"
        
        else: 
            Account.objects.create(username=username, password=password)

    return render(request, 'login.html', {'error': error_in_signup})

def logout_view(request):
    logout(request)
    return redirect('login_page')
