from django.shortcuts import render, redirect
from .models import Supplier, WaterBottle, Account
import logout 


# Create your views here.

def view_supplier(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/view_supplier.html', {'suppliers': supplier_objects})


def view_bottles(request):
    bottle_objects = WaterBottle.objects.all()
    return render(request, 'MyInventoryApp/view_bottles.html', {'bottles': bottle_objects})


def add_bottle(request):
    supplier_objects = Supplier.objects.all()
    return render(request, 'MyInventoryApp/add_bottle.html')

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
