
from django.urls import path
from . import views

app_name = 'network'

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:post_id>", views.post, name="post"),
    path("posts/<int:user_id>", views.posts, name="posts"),
    path("create-post", views.createPost, name="create-post"),
    path("remove-post/<int:id>", views.removePost, name="remove-post"),
    path("edit-post/<int:post_id>", views.edit, name="edit-post"),
    path("add-comment", views.addComment, name="add-comment"),

    path("profile/<int:user_id>", views.profile, name="profile"),
    path("edit-profile/", views.editProfile, name="edit-profile"),

    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),

    path("following", views.following, name="following"),


    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),

    path("ai", views.ai_generate, name="ai")
]
