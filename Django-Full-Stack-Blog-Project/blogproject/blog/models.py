from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
       return self.full_name()

class Tag(models.Model):
    caption = models.CharField(max_length=50)
    def __str__(self):
        return self.caption

class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=50)
    #image_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(validators=[MinLengthValidator(10)]) #For larger longer text
    slug = models.SlugField(unique=True, db_index=True) #django automaticlly Implies setting Field.db_index to True.
    #author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) #it transforms the title to slug
        super().save(*args, **kwargs) #it calls upper method so we will save at the end 


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(null=True)
    def __str__(self):
        return str(self.post) + ", " + self.text 

class Room(models.Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{str(self.room)} - {self.sender}"
