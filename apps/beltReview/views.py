from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from .models import User, Author, Book, Review

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
    # authors = Author.objects.all()
    # print 'AUTHORS'
    # for author in authors:
    #     print author
    # print
    # print 'BOOKS'
    # books = Book.objects.all()
    # for book in books:
    #     print book
    # print
    # print 'REVIEWS'
    # print book_reviews
    # for review in reviews:
    #     print review

    # print 'LIST HERE'
    # for review in reviews:
    #     print review.book.title
    book_reviews = []
    reviews = Review.objects.values_list('book_id', flat=True).distinct()
    for book_id in reviews:
        book_reviews.append(Book.objects.get(id=book_id).title)
    print book_reviews
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
        print 'inside no error if statement'
        return redirect('/reviews')
    return redirect('/add_review')
