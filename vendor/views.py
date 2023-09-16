from django.shortcuts import get_object_or_404, render, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_user_vendor
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