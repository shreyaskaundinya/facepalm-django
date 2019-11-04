from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# DJANGO USER MODEL :
# username
# first_name
# last_name
# password
# email
# is_staff
# Create your models here.


class UserProfile(models.Model):
    ''' this is the user profile + user authentication '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    contact = models.IntegerField(unique=True, blank=False)
    likes = models.IntegerField(default=0)
    picture = models.ImageField(
        upload_to='static/profile-pictures/', default='static/default.png')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + " " + str(self.id)


'''class UserProfilePicture(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="username")
    image = models.ImageField(
        upload_to='static/profile-pictures/', default='static/default.png')

    def __str__(self):
        return self.user.user.username'''


class Following(models.Model):
    ''' following log table of all users '''
    user_following = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="follower_user")  # LOGGED IN USER
    user_follower = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="following_user")  # THE USER LOGGED IN IS FOLLOWING THIS GUY
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{follower} is now following {following}".format(follower=self.user_following.user.username, following=self.user_follower.user.username)


class LoginLog(models.Model):
    ''' gets the login times of all users '''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return "{user} logged in at {time}".format(user=self.user, time=self.timestamp)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.timestamp = timezone.now()
        return super(LoginLog, self).save(*args, **kwargs)


# login to this user --
''' 
test1
test
'''
