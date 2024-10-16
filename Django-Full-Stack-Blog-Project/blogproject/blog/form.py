from django import forms
from .models import Comment, Post
from login.models import CustomUser
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #fields = []
        exclude = ["post","date"]
        labels = {
            "user_name":"Your Name",
            "user_email":"Your Email",
            "text":"Your Comment"
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["slug","author"]


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["slug","author"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
    