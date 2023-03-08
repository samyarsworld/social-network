from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    content = models.CharField(max_length=5000)
    likes = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    lang = models.CharField(max_length=10)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"This post is written by {self.owner.username} on {self.date.strftime('%D %B %Y %H:%M:%S')}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_is_following')
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_is_being_followed')

    def __str__(self):
        return f"{self.user} follows {self.user_follower}"

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True, blank=True, related_name='post_likes')

    def __str__(self):
        return f"{self.liker} liked {self.post}"

class PostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='network_user_comments')
    content = models.CharField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='network_post_comments')

    def __str__(self):
        return f'Written by {self.author}'