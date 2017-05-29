from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from .models import User, Author

def index(request):
    # User.objects.all().delete()
    # print User.objects.all()
    # Author.objects.create(first_name='George', last_name='Martin')
    # print Author.objects.all()
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
        return redirect('/reviews')
    for error in errors:
        messages.info(request, error)
    return redirect('/reviews')

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
        return redirect('/reviews')
    for error in errors:
        messages.info(request, error)
    return redirect('/')

def reviews(request):
    return render(request, 'beltReview/review.html')

def add_review(request):
    author = Author.objects.annotate(screen_name=Concat('first_name', V(' ('), 'last_name', V(')'), output_field=CharField())).get()
    return render(request, 'beltReview/add.html', context)

def add(request):
    postData = {
        'title': request.POST['title'],
        'authorID': request.POST['authorID'],
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }
    print postData
    return redirect('/add_review')
