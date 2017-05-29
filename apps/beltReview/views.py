from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    # User.objects.all().delete()
    print User.objects.all()
    return render(request, 'beltReview/index.html')

def register(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'alias': request.POST['alias'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
    }
    errors = User.objects.register(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.get(email=postData['email']).id
        request.session['name'] = postData['first_name']
        return redirect('/')
    for error in errors:
        messages.info(request, error)
    return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    print postData
    errors = User.objects.login(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.get(email=postData['email']).id
        request.session['name'] = User.objects.get(email=postData['email']).first_name
        return redirect('/')
    for error in errors:
        messages.info(request, error)
    return redirect('/')
