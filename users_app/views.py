from django.contrib import messages
from django.shortcuts import redirect, render

from users_app.forms import CustomRegisterForm


def register(request):
    if request.method == "POST":
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(
                request, "New User Account Created. Login To Get Started!")
            return redirect('register')
    else:
        register_form = CustomRegisterForm()

    context = {
        'register_form': register_form
    }
    return render(request, 'register.html', context)
