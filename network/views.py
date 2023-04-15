from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Follow, Like, PostComment
from authMain.models import Profile, User
import json
from django.http import JsonResponse
from django.db.models import Q

import os
from dotenv import load_dotenv
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.list()


languages = ['Python', 'Java', 'Javascript', 'SQL', 'C', 'Ruby', 'HTML']

def home(request):
    allPosts = Post.objects.all().order_by('date')
    pageNumber = request.GET.get('page')
    query = request.GET.get('search')
    if query:
        allPosts = allPosts.filter(Q(content__icontains=query) | Q(title__icontains=query) | Q(lang__icontains=query))
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
        'liked_posts': postsYouLiked,
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
def posts(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(owner=user).order_by('date')

    pageNumber = request.GET.get('page')
    p = Paginator(posts, 6)
    pagePosts = p.get_page(pageNumber)

    return render(request, "network/posts.html", {
        'posts': pagePosts,
        'page-num': pageNumber,
    })

@csrf_exempt
@login_required
def ai_generate(request):
    if request.method == 'POST':
        # Get user input from POST request
        prompt = request.POST.get('prompt')
        try:
            # text-davinci-003
            # Make API request to ChatGPT
            ai_response = openai.Completion.create(
                engine = 'gpt-3.5-turbo',
                prompt = prompt,
                max_tokens=100,
                temperature=0.5,
            )

            # Get response text from API response
            response_text = ai_response.choices[0].text
            return JsonResponse({'response':response_text})
        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'response':'Something went wrong'})

        
    

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
        userPosts = Post.objects.filter(owner=user).order_by('date')
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
    profile = Profile.objects.get(user=user)
    allPosts = Post.objects.filter(owner=user).order_by('date')
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
        'profile': profile,
        'posts': pagePosts,
        'following': following,
        'followers': followers,
        'isFollowing': isFollowing
    })


@login_required
def editProfile(request):
    if request.method == 'POST':
        data = request.POST
        profile = Profile.objects.get(user=request.user)
        if data['name']:
            profile.name = data['name']
        if data['last']:
            profile.last = data['last']
        if data['country']:
            profile.country = data['country']
        if data['education']:
            profile.education = data['education']
        if data['phone']:
            profile.phone = data['phone']
        if data['pic']:
            profile.pic = data['pic']
        if data['email']:
            profile.email = data['email']
        if data['about']:
            profile.about = data['about']
        profile.save()
        return redirect(reverse("network:profile", args=(request.user.id,)))

    profile = Profile.objects.get(user=request.user)
    return render(request, "network/edit_profile.html", {
        'profile': profile
    })


@login_required
def follow(request):
    if request.method == 'POST':
        userfollow = request.POST['userfollow']
        userToFollow = User.objects.get(username=userfollow)
        follow = Follow(user=request.user, user_follower=userToFollow)
        follow.save()
        user_id = userToFollow.id
        return redirect(reverse('network:profile', args=(user_id,)))


@login_required
def unfollow(request):
    if request.method == 'POST':
        userfollow = request.POST['userfollow']
        userToUnfollow = User.objects.get(username=userfollow)
        follow = Follow.objects.get(user=request.user, user_follower=userToUnfollow)
        follow.delete()
        user_id = userToUnfollow.id
        return redirect(reverse('network:profile', args=(user_id,)))


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









