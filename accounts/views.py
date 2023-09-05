from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages
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