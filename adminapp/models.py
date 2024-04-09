from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField()
    employee_count = models.IntegerField()
    company_location = models.CharField(max_length=255)
    document_proof = models.FileField(upload_to='images/')
    password = models.CharField(max_length=255)  # You can use Django's built-in password field for better security
    last_login_time=models.TimeField(null=True)
    last_login_date=models.DateField(null=True,auto_now_add=True) 
    no_of_times_login=models.IntegerField(null=True,default=0)
    date_time=models.DateTimeField(auto_now=True,null=True)
  

    def __str__(self):
        return self.company_name


class Security(models.Model):
    security_name = models.CharField(max_length=255)
    security_email = models.EmailField()   
    security_contact = models.CharField(max_length=20)
    security_document_proof = models.FileField(upload_to='security_documents/')
    security_password = models.CharField(max_length=255)  # You can use Django's built-in password field for better security
    security_last_login_time=models.TimeField(null=True)
    security_last_login_date=models.DateField(null=True,auto_now_add=True) 
    security_no_of_times_login=models.IntegerField(null=True,default=0)
    security_date_time=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.security_name
    



class CarNumber(models.Model):
    number = models.CharField(max_length=255)
    user_status = models.CharField(max_length=50, default='Authorized')

    def __str__(self):
        return self.number

  