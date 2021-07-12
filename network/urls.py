
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.self_profile, name="selfprofile"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("api/profile/<int:id>", views.profileapi, name="profileapi"),
    path("api/follower/<int:id>", views.followerapi, name="followerapi"),
    path("api/followed/<int:id>", views.followedapi, name="followedapi"),
    path("api/follow", views.followapi, name="followapi"),
    path("profilepic", views.profilepic, name="profilepic"),
    path("posts", views.posts, name="posts"),
    path("send", views.send, name="send"),
    path("like", views.like, name="like"),
    path("editpost", views.editpost, name="editpost"),
]
