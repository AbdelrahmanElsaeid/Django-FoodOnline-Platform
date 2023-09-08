from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from vendor.models import Vendor
# Create your views here.


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