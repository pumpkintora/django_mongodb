from django.db import models

# Create your models here.

# customer/employee
class User(models.Model):
    # unique
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=100)
    dob = models.DateField("Date of Birth", auto_now_add=True)
    nationality = models.CharField(max_length=50)
    citizenship = models.CharField(max_length=100)
    residence = models.CharField(max_length=200)
    identity_type = models.CharField(max_length=200)
    nric_no = models.CharField(max_length=200)
    passport_no = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    # link to other models
    account = models.ForeignKey(Account)

# company
class Account(models.Model):
    company_name = models.CharField(max_length=100)
    date_incorporation = models.DateField()
    company_address_1 = models.CharField(max_length=200)
    company_address_2 = models.CharField(max_length=200)
    # employees