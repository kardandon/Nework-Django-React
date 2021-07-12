from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
import json
from .models import *


def index(request):
    return render(request, "network/index.html")


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
        url = request.POST["url"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, profilepic_url=url)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request, id):
    pass

@login_required
def self_profile(request):
    return HttpResponseRedirect(reverse("profile", kwargs={"id": request.user.id}))

def profile(request, id):
    data = Posts.objects.filter(user=User.objects.get(pk=id)).all()
    posts = [{"is_user": dat.user.id == id,"postid": dat.id, "profilepic": dat.user.profilepic_url, "timestamp": str(dat.timestamp.strftime("%c")), "username": dat.user.username, "text": dat.body, "id": dat.user.id, "likes": len(dat.likes.all())} for dat in data]
    return render(request, "network/profile.html",{"posts": posts})

def profileapi(request, id):
    data = User.objects.get(pk=id).serialize()
    x = request.user.is_authenticated
    y = request.user.id != id
    if (x and y):
        data["follow_text"]="Unfollow" if request.user.is_followed(User.objects.get(pk=id))  else "Follow"
        data["user"] = True
    elif(x and not y):
        data["change_profile_pic"] = True
    return JsonResponse(data)

def followerapi(request,id):
    try:
        q = int(request.GET.get("q"))
        w = int(request.GET.get("w"))
    except:
        q=0
        w=10
    if not q: q = 0
    if not w: w = 10
    return JsonResponse(User.objects.get(pk=id).serialize_follower(q,w))

def followedapi(request,id):
    try:
        q = int(request.GET.get("q"))
        w = int(request.GET.get("w"))
    except:
        q=0
        w=10
    if not q: q = 0
    if not w: w = 10
    return JsonResponse(User.objects.get(pk=id).serialize_follows(q,w))

@csrf_exempt
@login_required
def followapi(request):
    if request.method != "PUT":
        return JsonResponse({"error": "need to use post"}, status=400)
    try:
        id = int(json.loads(request.body)["id"])
        if id == request.user.id: raise Exception()
    except Exception as e:
        return JsonResponse({"error": "need to get valid id"}, status=400)
    request.user.toggle_follow(User.objects.get(pk=id))
    return JsonResponse({"error": ""}, status=201)

def profilepic(request):
    if request.method == "POST":
        url = request.POST["url"]
        request.user.profilepic_url = url
        request.user.save()
        return HttpResponseRedirect(reverse("profilepic"))
    elif request.method == "GET":
        return render(request, "network/profilepic.html",{
            "url": request.user.profilepic_url,
        })
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

def posts(request):
    try:
        q = int(request.GET.get("q"))
        w = int(request.GET.get("w"))
        e = int(request.GET.get("e"))
        f = (request.GET.get("f"))
        data = []
        if f == "follower":
            data = Posts.objects.filter(user__in=request.user.followed.all()).order_by("-timestamp")[q:q+w]
        else:
            if e == 0:
                data = Posts.objects.filter().order_by("-timestamp")[q:q+w]
            else:
                data = Posts.objects.filter(user=User.objects.get(pk=e)).order_by("-timestamp")[q:q+w]
        if request.user.is_authenticated:
            id = request.user.id
        else:
            id = 0
        data = [{"is_user": dat.user.id == id,"postid": dat.id, "profilepic": dat.user.profilepic_url, "timestamp": str(dat.timestamp.strftime("%c")), "username": dat.user.username, "text": dat.body, "id": dat.user.id, "likes": len(dat.likes.all())} for dat in data]
        return JsonResponse({"data": data}, status=201)
    except:
        return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def send(request):
    try:
        text = json.loads(request.body).get("text")
        Posts.objects.create(user=request.user, body=text).save()
        return JsonResponse({"error": ""}, status=201)
    except Exception as e:
        return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def like(request):
    try:
        id = int(json.loads(request.body).get("id"))
        Posts.objects.get(pk=id).toggle_like(request.user)
        return JsonResponse({"error": ""}, status=201)
    except:
        return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def editpost(request):
    try:
        id = int(json.loads(request.body).get("id"))
        text = str(json.loads(request.body).get("text"))
        post = Posts.objects.get(pk=id, user=request.user)
        post.body = text
        post.timestamp = datetime.datetime.utcnow()
        post.save()
        return JsonResponse({"error": ""}, status=201)
    except:
        return JsonResponse({"error": "Invalid request"}, status=400)