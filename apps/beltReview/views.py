from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from .models import User, Author, Book, Review
from django.http import HttpResponseRedirect

def index(request):
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
    errors = User.objects.login(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.get(email=postData['email']).id
        request.session['name'] = User.objects.get(email=postData['email']).first_name
        return redirect('/reviews')
    for error in errors:
        messages.info(request, error)
    return redirect('/')

def reviews(request):
    book_reviews = []
    for review in Review.objects.raw("SELECT * FROM beltreview_review GROUP BY book_id"):
        book_reviews.append(review)
    context = {
        'reviews': Review.objects.all().order_by('-created_at')[:3],
        'book_reviews': book_reviews,
    }
    return render(request, 'beltReview/review.html', context)

def add_review(request):
    authors = Author.objects.annotate(name=Concat('first_name',V(' '),'last_name')).order_by('last_name')
    context = {
        'authors': authors,
    }
    return render(request, 'beltReview/add.html', context)

def add(request):
    postData = {
        'title': request.POST['title'],
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'review': request.POST['review'],
        'rating': request.POST['rating'],
        'user_id': request.session['id'],
    }
    errors = Author.objects.check_review(postData)
    print 'ERRORS:', errors
    if len(errors) == 0:
        return redirect('/reviews')
    return redirect('/add_review')

def book_info(request, id):
    context = {
        'reviews': Review.objects.filter(book_id=id).order_by('-created_at'),
        'books': Book.objects.get(id=id),
    }
    return render(request, 'beltReview/bookinfo.html', context)

def add_book_review(request, id):
    postData = {
        'review': request.POST['review'],
        'rating': request.POST['rating'],
        'book_id': id,
        'user_id': request.session['id'],
    }
    errors = Review.objects.simple_check(postData)
    if len(errors) > 0:
        messages.info(request, errors[0])
    # return to current page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete(request, id):
    Review.objects.get(id=id).delete()
    return redirect('/reviews')

def users(request, id):
    my_reviews = []
    for review in Review.objects.raw("SELECT * FROM beltreview_review LEFT JOIN beltreview_book ON beltreview_review.book_id = beltreview_book.id WHERE beltreview_review.user_id = %s GROUP BY beltreview_book.title", [id]):
        my_reviews.append(review)
    context = {
        'user': User.objects.get(id=id),
        'reviews': Review.objects.filter(user_id=id).count(),
        'my_reviews': my_reviews,
    }
    return render(request,'beltReview/user.html', context)
