from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, Like
import json
from django.http import JsonResponse

def index(request):
    allPosts = Post.objects.all()
    pageNumber = request.GET.get('page')
    p = Paginator(allPosts, 10)
    pagePosts = p.get_page(pageNumber)
    
    try:
        allYourLikes = Like.objects.filter(liker=request.user)
        postsYouLiked = list(map(lambda x : x.post, allYourLikes))
    except:
        postsYouLiked = []
    
    return render(request, "network/index.html", {
        'posts': pagePosts,
        'page-num': pageNumber,
        'liked_posts': postsYouLiked
    })


@login_required
@csrf_exempt
def like(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)   
        newLike = Like(liker=request.user, post=post)
        post.likes = post.likes + 1
        post.save()
        newLike.save()
        return JsonResponse({"message": "Like successful"})


@login_required
@csrf_exempt
def unlike(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        like = Like.objects.get(post=post)
        post.likes = post.likes - 1
        post.save()
        like.delete()
        return JsonResponse({"message": "Like removed"})


@login_required
def edit(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.get(id=post_id)
        post.content = data['content']
        post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})


@login_required
def following(request):
    following = Follow.objects.filter(user=request.user)
    follwingPosts = []

    for each in following:
        user = each.user_follower
        userPosts = Post.objects.filter(owner=user)
        follwingPosts.extend(userPosts)

    pageNumber = request.GET.get('page')
    p = Paginator(follwingPosts, 10)
    pagePosts = p.get_page(pageNumber)

    try:
        allYourLikes = Like.objects.filter(liker=request.user)
        postsYouLiked = list(map(lambda x : x.post, allYourLikes))
    except:
        postsYouLiked = []

    return render(request, "network/following.html", {
        'posts': follwingPosts,
        'page-num': pageNumber,
        'liked_posts': postsYouLiked
    })


@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    allPosts = Post.objects.filter(owner=user)
    pageNumber = request.GET.get('page')
    p = Paginator(allPosts, 10)
    pagePosts = p.get_page(pageNumber)

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    try:
        checkFollow = followers.filter(user=request.user)
        if len(checkFollow): isFollowing = True
        else: isFollowing = False
    except:
        isFollowing = False

    return render(request, "network/profile.html", {
        'user_profile': user,
        'posts': pagePosts,
        'following': following,
        'followers': followers,
        'isFollowing': isFollowing
    })


@login_required
def follow(request):
    if request.method == 'POST':
        userfollow = request.POST['userfollow']
        userToFollow = User.objects.get(username=userfollow)
        follow = Follow(user=request.user, user_follower=userToFollow)
        follow.save()
        user_id = userToFollow.id
        return redirect(reverse('profile', args=(user_id,)))


@login_required
def unfollow(request):
    if request.method == 'POST':
        userfollow = request.POST['userfollow']
        userToUnfollow = User.objects.get(username=userfollow)
        follow = Follow.objects.get(user=request.user, user_follower=userToUnfollow)
        follow.delete()
        user_id = userToUnfollow.id
        return redirect(reverse('profile', args=(user_id,)))


@login_required
def createPost(request):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post(content=content, owner=request.user)
        post.save()
        return redirect('index')


@login_required
def removePost(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('index')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
