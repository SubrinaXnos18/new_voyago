from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
    name = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='packages/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Entry - {self.created_at.strftime('%Y-%m-%d')}"

class DiaryImage(models.Model):
    diary = models.ForeignKey(Diary, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='diary/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.diary}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"
