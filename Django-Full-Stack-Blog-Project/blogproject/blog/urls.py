from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path("",views.StartingPageView.as_view(),name="starting-page"),
    path("posts", views.AllPosts.as_view(), name="post-page"),
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post-detail-page"), 
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("create-a-post",views.CreatePostView.as_view(),name="create-a-post"),
    path("my-posts",views.MyPostsView.as_view(), name="my-posts"),
    path("posts/edit/<slug:slug>", views.EditPostView.as_view(), name = "edit-post"),
    path("posts/delete/<slug:slug>",views.DeletePostView.as_view(), name = "delete-post"),
    path("profile/<int:pk>",views.ProfileView.as_view(),name="profile"),
    path('xd', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
]
