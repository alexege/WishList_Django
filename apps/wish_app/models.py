from __future__ import unicode_literals
from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if postData['password'] != postData['confirmation_password']:
            errors["password"] = "Passwords do not match"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Item name must be at least three characters long"
        if len(postData['description']) < 3:
            errors['description'] = "Item description must be at least three characters long"
        return errors

class Wish(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="wished")
    users_who_liked = models.ManyToManyField(User, related_name="wishes")
    objects = WishManager()