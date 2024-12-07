from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name
    
class Ward(models.Model):
    ward_no = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.ward_no


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=6)
    country = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=12, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=20, null=True, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))

    def __str__(self):
        return self.username
    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    user_type = models.CharField(max_length=100, choices=[('Doctor', 'Doctor'), ('Nurse', 'Nurse'), ('HOD', 'HOD'), ('Principal', 'Principal'), ('Admin', 'Admin')])
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    ward = models.CharField(max_length=30)
    def __str__(self):
        return self.user.name
    
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='patient', null=True)
    ward = models.CharField(max_length=100)
    admit = models.DateTimeField(null=True)
    discharge = models.DateTimeField(null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

class Logs(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='updated_by')
    last_updated_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='last_updated_by')
    log = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Connection(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    private = models.BooleanField(default=False)
    SOS = models.BooleanField(default=True)
    listed = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

