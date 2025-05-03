from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        return render(request, 'users/register.html', {'form':UserCreationForm()})

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})