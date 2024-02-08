from django.shortcuts import render
from django.contrib.auth import get_user

def main_view(request):
    return render(request, 'main_template.html')

def home_view(request):
    return render(request, 'home_template.html')

def navbar_view(request):
    user = get_user(request)
    return render(request, 'navbar.html', {'user': user})


def sidebar_view(request):
    user = get_user(request)
    return render(request, 'sidebar.html', {'user': user})

def queue_view(request):
    return render(request, 'queue.html')
