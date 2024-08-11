from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages
from django.views.generic import ListView
from .forms import ItemForm, ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404, render, redirect)
from django.contrib import messages
from .models import *
from django.db.models import Q


class IndexView(ListView):
    template_name = 'index.html'
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all()

@login_required
def FoundView(request):
    item = get_object_or_404(Item, pk=request.POST['item'])
    item.found = True
    item.save()
    return redirect('index')


@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.creator_username = request.user.username
            item.save()
            return redirect('index')  # Redirect to the index page after successful form submission
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item.html', {'item': item})


@login_required
def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form})


@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('index')
    return render(request, 'item_delete.html', {'item': item, 'confirm_delete': True})


def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')


def my_registration_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken")
            check = "taken"
            context = {
                'check': check
            }
            return render(request, 'registration.html', context)

        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_staff = True
        myuser.save()

        check = ""
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            check = "taken"
            context = {
                'check': check
            }
            return render(request, 'base.html', context)

        messages.success(request, "Your account has been signed up successfully!")
        return redirect('login')

    return render(request, "registration.html")


def my_logout_view(request):
    logout(request)
    return redirect('login')


def search_items(request):
    query = request.GET.get('query')
    if query:
        items = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        items = Item.objects.all()
    return render(request, 'search_results.html', {'items': items, 'query': query})


def about_us(request):
    return render(request, 'about.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


@csrf_exempt
def home(request):
    return render(request, 'home.html')