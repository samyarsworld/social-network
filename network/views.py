from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from network.decorators import unauthenticated_user
from .models import User, Post, Follow, Like, PostComment
import json
from django.http import JsonResponse

languages = ['Python', 'Java', 'Javascript', 'SQL', 'C', 'Ruby', 'HTML']

def home(request):
    allPosts = Post.objects.all()
    pageNumber = request.GET.get('page')
    p = Paginator(allPosts, 6)
    pagePosts = p.get_page(pageNumber)
    
    try:
        allYourLikes = Like.objects.filter(liker=request.user)
        postsYouLiked = list(map(lambda x : x.post, allYourLikes))
    except:
        postsYouLiked = []
    
    return render(request, "network/home.html", {
        'posts': pagePosts,
        'languages': languages,
        'page-num': pageNumber,
        'liked_posts': postsYouLiked
    })


@login_required
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = PostComment.objects.filter(post=post)
    return render(request, "network/post.html", {
        'post': post,
        'comments': comments
    })


@login_required
def addComment(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)
        content = request.POST['comment']
        comment = PostComment(content=content, post=post, author=request.user)
        comment.save()
        return redirect(reverse('network:post', args = (post.id,)))


@login_required
@csrf_exempt
def like(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)   
        newLike = Like(liker=request.user, post=post)
        post.likes = post.likes + 1
        post.save()
        newLike.save()
        return JsonResponse({"message": post.likes})


@login_required
@csrf_exempt
def unlike(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        like = Like.objects.get(post=post)
        post.likes = post.likes - 1
        post.save()
        like.delete()
        return JsonResponse({"message": post.likes})


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
        try: 
            content = request.POST['content']
            title = request.POST['title']
            lang = request.POST['lang']
        except:
            return redirect('network:home')

        if lang not in languages or not title or not content:
            return redirect('network:home')

        post = Post(content=content, owner=request.user, title=title, lang=lang)
        post.save()
        
        return redirect('network:home')


@login_required
def removePost(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('network:home')






@unauthenticated_user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:home"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:home"))

@unauthenticated_user
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
        return HttpResponseRedirect(reverse("network:home"))
    else:
        return render(request, "network/register.html")


