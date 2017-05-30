from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        # Check whether email exists in db
        if User.objects.filter(email=postData['email']):
            errors.append('Email is already registered')
        # Validate first name
        if len(postData['first_name']) < 2:
            errors.append('First name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['first_name']):
            errors.append('First name must only contain alphabet')
        # Validate last name
        if len(postData['last_name']) < 2:
            errors.append('Last name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['last_name']):
            errors.append('Last name must only contain alphabet')
        # Validate alias
        if len(postData['alias']) < 2:
            errors.append('Alias must be at least 2 characters')
        elif not NAME_REGEX.match(postData['alias']):
            errors.append('Alias must only contain alphabet')
        # Validate email
        if len(postData['email']) < 1:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append('Invalid email format')
        # Validate password
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        # Validate confirm password
        elif postData['password'] != postData['confirm']:
            errors.append('Passwords do not match')

        # if no errors
        if len(errors) == 0:
            # Generate new salt
            salt = bcrypt.gensalt()
            # Form data must be encoded before hashing
            password = postData['password'].encode()
            # Hash pw with password and salt
            hashed_pw = bcrypt.hashpw(password, salt)
            # add to database
            User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], alias=postData['alias'], email=postData['email'], password=hashed_pw)

        return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(email=postData['email']):
            form_pw = postData['password'].encode()
            db_pw = User.objects.get(email=postData['email']).password.encode()
            print db_pw
            # if hashed passwords do not match
            if not bcrypt.checkpw(form_pw, db_pw):
                errors.append('Incorrect password')
        # else if email is not found in db
        else:
            errors.append('Email has not been registered')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + ' ' + self.last_name + ' - ' + self.alias + ' - ' + self.email + ' - ' + self.password

class AuthorManager(models.Manager):
    def check_review(self, postData):
        errors = []
        # Validate book title
        if len(postData['title']) < 2:
            errors.append('Title must be at least 2 characters')
        # Validate review
        if len(postData['review']) < 10:
            errors.append('Review must be at least 10 characters')
        # Validate first_name
        if len(postData['first_name']) < 2:
            errors.append('First name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['first_name']):
            errors.append('First name can only be alphabet')
        # Validate last_name
        if len(postData['last_name']) < 2:
            errors.append('Last name must be at least 2 characters')
        elif not NAME_REGEX.match(postData['last_name']):
            errors.append('Last name can only be alphabet')

        if len(errors) == 0:
            author = Author.objects.filter(first_name=postData['first_name'], last_name=postData['last_name'])
            title = Book.objects.filter(title=postData['title'])
            # If author and book title already exist, only update Review table
            if author.count() and title.count():
                book_id = Book.objects.filter(title=postData['title'], author_id=author[0].id)[0].id
                Review.objects.create(review=postData['review'], rating=postData['rating'], user_id=postData['user_id'], book_id=book_id)
            # If author already exists, add new book to Book table and update Review
            elif author.count():
                Book.objects.create(title=postData['title'], author_id=author[0].id)
                Review.objects.create(review=postData['review'], rating=postData['rating'], user_id=postData['user_id'], book_id=Book.objects.latest('id').id)
            # If author does not exist, update Author, Book, and Review
            else:
                Author.objects.create(first_name=postData['first_name'],last_name=postData['last_name'])
                Book.objects.create(title=postData['title'], author_id=Author.objects.latest('id').id)
                Review.objects.create(review=postData['review'], rating=postData['rating'], user_id=postData['user_id'], book_id=Book.objects.latest('id').id)

        return errors
        # If user doesn't enter a name, use the author in dropdown menu
        # else:


class Author(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuthorManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + ' - ' + self.last_name

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.title + ' - ' + str(self.author_id)

class ReviewManager(models.Manager):
    def simple_check(self, postData):
        errors = []
        if len(postData['review']) < 10:
            errors.append('Review must be at least 10 characters')
        else:
            Review.objects.create(review=postData['review'], rating=postData['rating'], user_id=postData['user_id'], book_id=postData['book_id'])
        return errors

class Review(models.Model):
    review = models.TextField(max_length=1000)
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name='reviews')
    book = models.ForeignKey(Book, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.review + ' - ' + str(self.rating) + ' - ' + str(self.user_id) + ' - ' + str(self.book_id)
