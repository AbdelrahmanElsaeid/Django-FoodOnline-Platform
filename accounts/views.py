from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib.auth import login , authenticate, logout as logoutUser
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.


def check_user_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
def check_user_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('registerUser')
    form =UserForm()

    context = {
        'form':form
    } 
    return render(request, 'accounts/registerUser.html', context)



def registerVendor(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user=user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            
            print('invalid form')
            print(form.errors)

    else:
        form =UserForm()
        v_form = VendorForm()

    context = {
        'form':form,
        'v_form':v_form
    } 
    return render(request, 'accounts/registerVendor.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged.')
            return redirect('myAccount')
        else:
            messages.error(request,'Username or Password does not exist')
            return redirect('login')

    return render(request, 'accounts/login.html')



def logout(request):
    logoutUser(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

    return render


@login_required(login_url='login')
@user_passes_test(check_user_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_user_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')