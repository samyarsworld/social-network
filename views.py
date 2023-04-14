from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from agora_token_builder import RtcTokenBuilder
import random
import time
from .models import User, RoomMember, Profile, ChatMessage, Friend
from .forms import ChatMessageForm
import json
from django.http import JsonResponse


def getToken(request):
    appId = "8468c05907164599aafc8b3ea51d061f"
    appCertificate = "689af080383143b39eaf9562c0bae814"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)


def chatMain(request):
    chats = ChatMessage.objects.all()
    user_profile = Profile.objects.get(user=request.user)
    f = Friend.objects.filter(user=request.user)
    friends = []
    try:
        users = list(map(lambda x: x.user_friend, f))
        for each in users:
            friends.append(Profile.objects.get(user=each))
    except:
        friends = []
   
    return render(request, "videochat/chatMain.html", {
        'user_profile': user_profile,
        'friends': friends
    })


def chat(request, pk):
    friend = User.objects.get(id=pk)
    user_profile = Profile.objects.get(user=request.user)
    friend_profile = Profile.objects.get(user=friend)

    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=friend_profile, msg_receiver=user_profile, seen=False)
    rec_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user_profile
            chat_message.msg_receiver = friend_profile
            chat_message.save()
            return redirect(reverse("chat",  args=(pk,)))
    return render(request, "videochat/chat.html", {
        "form": form,
        "friend_profile":friend_profile,
        "chats": chats,
        "user_profile": user_profile,
        "num": rec_chats.count()
    })


def sentMessages(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    friend_profile = Profile.objects.get(user=User.objects.get(id=pk))
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user_profile, msg_receiver=friend_profile, seen=False )
    return JsonResponse(new_chat_message.body, safe=False)

def receivedMessages(request, pk):
    user_profile = request.user.user_profile
    friend_profile = Profile.objects.get(user=User.objects.get(id=pk))
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=friend_profile, msg_receiver=user_profile)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)

def chatNotification(request):
    user_profile = request.user.user_profile
    friends = Friend.objects.filter(user=request.user)
    arr = []
    for friend in friends:
        friend_profile = Profile.objects.get(user=friend.user_friend)
        chats = ChatMessage.objects.filter(msg_sender=friend_profile, msg_receiver=user_profile, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)


def main(request):
    return render(request, "videochat/main.html")

def community(request):
    all = User.objects.all()
    friends = Friend.objects.filter(user=request.user)
    try:
        friends_user = list(map(lambda x: x.user_friend, friends))
    except:
        friends_user = []

    return render(request, "videochat/community.html", {
        'all': all,
        'friends': friends_user
    })

def friends(request):
    friends = Friend.objects.filter(user=request.user)
    try:
        friends_user = list(map(lambda x: x.user_friend, friends))
    except:
        friends_user = []
    
    return render(request, "videochat/friends.html", {
        'friends': friends_user
    })


def add(request, friend_id):
    f1 = Friend(user=request.user, user_friend=User.objects.get(id=friend_id))
    f1.save()
    f2 = Friend(user=User.objects.get(id=friend_id), user_friend=request.user)
    f2.save()

    return redirect("community")

def remove(request, friend_id):
    f1 = Friend.objects.get(user=request.user, user_friend=User.objects.get(id=friend_id))
    f1.delete()
    f2 = Friend.objects.get(user=User.objects.get(id=friend_id), user_friend=request.user)
    f2.delete()

    return redirect("community")



def lobby(request):
    return render(request, "videochat/lobby.html")


def room(request):
    return render(request, "videochat/room.html")

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)
    return render(request, "videochat/profile.html", {
        'user_profile': user_profile
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

        return redirect(reverse("profile", args=(request.user.id,)))


    user_profile = Profile.objects.get(user=request.user)
    return render(request, "videochat/editProfile.html", {
        'user_profile': user_profile
    })

@login_required
def video(request):
    return render(request, "videochat/video.html")



# Authentication views
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("main"))
        else:
            return render(request, "videochat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "videochat/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "videochat/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "videochat/register.html", {
                "message": "Username already taken."
            })
        profile = Profile(user=user)
        profile.save()

        login(request, user)
        return HttpResponseRedirect(reverse("main"))
    else:
        return render(request, "videochat/register.html")
