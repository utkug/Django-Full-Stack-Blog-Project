from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

# Create your views here.

from .models import Post, Comment
from login.models import CustomUser
from .form import CommentForm, PostForm, EditForm, ProfileForm   

#all_posts = Post.objects.all().order_by("-date")

def get_date(post):
    return post['date']

def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3] # - desccanding, first 3 posts
    return render(request, "blog/index.html", {
        "posts":latest_posts
    })

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html",{
        "all_posts":all_posts
    })

def post_detail(request, slug):
#    identified_post = next(post for post in all_posts if post['slug']==slug) #next element 
    #identified_post = Post.objects.get(slug=slug)
    identified_post = get_object_or_404(Post, slug = slug)
    return render(request, "blog/post-detail.html",{
        "post":identified_post,
        "post_tags":identified_post.tags.all()
    })

class AllPosts(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"
    ordering = ["-date"]

    


# class PostDetail(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post

#     def get_context_data(self, **kwargs: Any):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all() 
#         context["comment_form"] = CommentForm()
#         return context
    
class PostDetail(View):
    # template_name = "blog/post-detail.html"
    # model = Post

    def is_stored_posts(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        user_auth = request.user

        if user_auth.is_authenticated:
            comment_form_initial = CommentForm(initial={
                "user_name": user_auth.username,
                "user_email": user_auth.email
            })
        else:
            comment_form_initial = CommentForm()


        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form_initial,
            "comments":post.comments.all().order_by("-date"),
            "saved_for_later": self.is_stored_posts(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST) #it contains submitted data
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False) #we can call save on that form because it based modelForm
            #commit, calling save won't hit the db it will create a new model instance 
            comment.post = post
            comment.date = timezone.now()
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
            #return HttpResponseRedirect(request.path)

        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments":post.comments.all().order_by("-date"),
            #"comments":post.comments.all().order_by("-id")
            "saved_for_later": self.is_stored_posts(request, post.id)
        }    
        return render(request, "blog/post-detail.html", context)

    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all() 
    #     context["comment_form"] = CommentForm()
    #     return context    
    


class StartingPageView(LoginRequiredMixin, ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]
    login_url = "login/login"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class ReadLaterView(View):
    def get(self, request):
        stored_post = request.session.get("stored_posts")

        context = {}

        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_post) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html",context)
    def post(self, request):
        stored_post = request.session.get("stored_posts")

        if stored_post is None:
            stored_post = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session["stored_posts"] = stored_post    

        return HttpResponseRedirect("/")

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post    
    template_name = "blog/create-a-post.html"
    form_class = PostForm
    success_url = "/"
    login_url = "login/login"


    def form_valid(self, form):
        form.instance.author = self.request.user
        
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']

        return super().form_valid(form)
    


class MyPostsView(LoginRequiredMixin,ListView):
    template_name = "blog/my-posts.html"
    model = Post
    ordering = ["-date"]
    login_url = "login/login"
    context_object_name = "my_posts" #html deki ismi belirliyor

    def get_queryset(self):
        my_posts = Post.objects.filter(author = self.request.user)
        return my_posts
    


class EditPostView(LoginRequiredMixin, UpdateView):
    template_name = "blog/edit-post.html"
    model = Post
    form_class = EditForm
    login_url = "login/login"    

    def get_success_url(self):
        return reverse_lazy('post-detail-page', kwargs={'slug': self.object.slug})
    


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    login_url = "login/login"
    success_url = "/"
    template_name = "blog/edit-post.html"

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "blog/my-profile.html"
    form_class = ProfileForm
    model = CustomUser




def index(request):
    return render(request, 'blog/index2.html')

def room(request, room_name):
    return render(request, 'blog/room.html', {
        'room_name': room_name
    })