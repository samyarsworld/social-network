
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create-post", views.createPost, name="create-post"),
    path("remove-post/<int:id>", views.removePost, name="remove-post"),

    path("profile/<int:user_id>", views.profile, name="profile"),

    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),

    path("following", views.following, name="following"),

    path("edit/<int:post_id>", views.edit, name="edit"),

    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike")

]
