from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorForm, OpeningHoursForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_user_vendor
from menu.forms import CategoryForm, FooditemForm
from django.template.defaultfilters import slugify
from django.db import IntegrityError

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
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Added successfully.")
            return redirect('menu_builder')
        else:
            print(form.errors)
        
    else:        
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request,'vendor/add_category.html', context)


def edit_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category =get_object_or_404(Category, pk=pk)
    if request.method=="POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "Category Added successfully.")
            return redirect('menu_builder')
        else:
            print(form.errors)
        
    else:        
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category
    }
    return render(request,'vendor/edit_category.html', context)


def delete_category(request, pk=None):
    category =get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,"category deleted")
    return redirect('menu_builder')   



def add_food(request):
    vendor = Vendor.objects.get(user=request.user)
    #category = Category.objects.get(vendor=vendor)
    if request.method=="POST":
        form = FooditemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            fooditem = form.save(commit=False)
            fooditem.vendor = vendor
           # fooditem.category = category
            fooditem.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food Item Added successfully.")
            return redirect('menu_builder')
        else:
            print(form.errors)
        
    else:        
        form = FooditemForm()
        form.fields['category'].queryset=Category.objects.filter(vendor=vendor)
    context = {
        'form':form
    }

    return render(request,'vendor/add_food.html', context)





def edit_food(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    food =get_object_or_404(FoodItem, pk=pk)
    if request.method=="POST":
        form = FooditemForm(request.POST, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']        
            food = form.save(commit=False)
            food.vendor = vendor
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Category Added successfully.")
            return redirect('fooditems_by_category', food.category.id )
        else:
            print(form.errors)
        
    else:        
        form = FooditemForm(instance=food)
        form.fields['category'].queryset=Category.objects.filter(vendor=vendor)
    context = {
        'form':form,
        'food':food
    }
    return render(request,'vendor/edit_food.html', context)



def delete_food(request, pk=None):
    food =get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request,"food deleted")
    return redirect('fooditems_by_category', food.category.id )


def opening_hours(request):
    vendor = Vendor.objects.get(user=request.user)
    opening_hours = OpeningHour.objects.filter(vendor=vendor)
    form = OpeningHoursForm()


    context={
        'opening_hours': opening_hours,
        'form': form

    }
    return render(request, 'vendor/opening_hours.html', context)    

def add_opening_hours(request):
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(user=request.user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method=="POST":
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            try:
                hour = OpeningHour.objects.create(vendor=vendor, day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response={'status': 'success', 'id':hour.id, 'day':day.get_day_display(), 'is_closed': 'closed'}
                    else:
                        response={'status': 'success', 'id':hour.id, 'day':day.get_day_display(), 'from_hour':hour.from_hour, 'to_hour':hour.to_hour}

                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+' already exists for this day!'}
                return JsonResponse(response)

    return HttpResponse('add opening')


def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(user=request.user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id':pk})