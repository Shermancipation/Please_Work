from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import hashlib
import binascii
from os import urandom

class UserManager(models.Manager):
    def user_validation(self, postData):
        errors = []

        if len(postData['name']) < 3:
            errors.append("Name must be at least 3 characters.")
        if len(postData['username']) < 3:
            errors.append("Username must be at least 3 characters.")

        try:
            User.objects.get(username = postData['username'])
            errors.append("Username has already been registered.  Please choose a different username.")
        except:
            pass

        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 charaters.")
        if len(postData['confirm']) < 1:
            errors.append("Please confirm your password")
        if not postData["password"] == postData["confirm"]:
            errors.append("Your passwords do not match")


        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            hashed_password = hashlib.md5(postData['password'].encode('utf-8')).hexdigest();
            user = self.create(name=postData['name'], username=postData['username'], password=hashed_password, date_hired=postData['hire_date'])
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

    def login_validation(self, postData):
        login_errors = []

        try:
            User.objects.get(username=postData["username"])
            print ("$"*20 + "Username matches database entry.")
        except:
            login_errors.append("Email incorrect.")
        try:
            User.objects.get(username=postData["username"]).password == postData["password"]
            print ('%'*20 + "Username and password match database entry.")
        except:
            login_errors.append("Password incorrect.")

        response_to_views = {}
        if login_errors:
            response_to_views['status'] = False
            response_to_views['errors'] = login_errors
        else:
            user = User.objects.get(username=postData["username"])
            response_to_views['status'] = True
            response_to_views['user'] = user
        return response_to_views

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length = 100)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
