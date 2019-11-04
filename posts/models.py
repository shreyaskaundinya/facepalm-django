from django.db import models
from users import models as u_models
# Create your models here.


class Post(models.Model):
    user_profile = models.ForeignKey(
        u_models.UserProfile, on_delete=models.CASCADE)
    header = models.CharField(max_length=100)
    text = models.TextField(max_length=1000, blank=False)
    image = models.ImageField(upload_to=None)  # change this shit
    link = models.URLField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=20)
    post_topic = models.CharField(max_length=30)

    def __str__(self):
        return self.header
