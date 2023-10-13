from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    document = CloudinaryField('image')
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Document(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')

    def __str__(self) -> str:
        return self.title


class UploadFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to='images')

    def __str__(self) -> str:
        return self.title


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')

    def __str__(self) -> str:
        return self.name


class DocumentUpload(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering: ['-date']

