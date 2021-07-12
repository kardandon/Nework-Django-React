from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    profilepic_url = models.CharField(max_length=128)
    follower = models.ManyToManyField("User",related_name="followedby")
    followed = models.ManyToManyField("User",related_name="followsto")

    def serialize(self):
        return {
            "profilepic" : self.profilepic_url,
            "username" : self.username,
            "follower": len(self.follower.all()),
            "follows": len(self.followed.all()),
        }
    def serialize_follower(self,q,w):
        return {
            "list": [(user.username,user.id, user.profilepic_url) for user in self.follower.all()[q:w+q]],
        }
    def serialize_follows(self,q,w):
        return {
            "list": [(user.username,user.id, user.profilepic_url) for user in self.followed.all()[q:w+q]]
        }
    def is_followed(self, user):
        return user in self.followed.all()

    def is_follower(self, user):
        return user in self.follower.all()

    def toggle_follow(self, user):
        if self.is_followed(user):
            self.followed.remove(user)
            user.follower.remove(self.id)
        else:
            self.followed.add(user)
            user.follower.add(self.id)
        self.save()
        user.save()

class Posts(models.Model):
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def serialize(self):
        return {
            "timestamp" : self.timestamp,
            "body": self.body,
            "likes": len(self.likes.all())
        }
    def is_liked(self, user):
        return user in self.likes.all()
    
    def toggle_like(self, user):
        if self.is_liked(user):
            self.likes.remove(user)
        else:
            self.likes.add(user)
        self.save()
