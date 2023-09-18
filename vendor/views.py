from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_user_vendor
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
# Create your views here.


@login_required(login_url='login')
@user_passes_test(check_user_vendor)
def vprofile(request):

    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor, user =request.user)

    if request.method=="POST":
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if vendor_form.is_valid() and profile_form.is_valid():
            vendor_form.save()
            profile_form.save()
            messages.success(request, 'Settings update.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:

        vendor_form = VendorForm(instance=vendor)
        profile_form = UserProfileForm(instance=profile)
    context = {'vendor_form': vendor_form,
               'profile_form':profile_form,
               'profile':profile,
               'vendor':vendor}

    return render(request,'vendor/vprofile.html', context)




def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor)

    context={
        'categories':categories,
    }
    return render(request, 'vendor/menu_builder.html', context)



def fooditems_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


def add_category(request):
    vendor = Vendor.objects.get(user=request.user)
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slu
            form.save()
            messages.success(request, "Category Added successfully.")
            return redirect('menu_builder')
        
    else:        
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request,'vendor/add_category.html', context)