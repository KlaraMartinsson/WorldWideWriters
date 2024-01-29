from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))
CONTINENT = (
    (0, "None"), (1, "North America"), (2, "South America"), (3, "Africa"), (4, "Europe"), (5, "Asia"), (6, "Oceania"), (7, "Antarctica"))


# Create your models here.
class Post(models.Model):
    """
    Database model for posts
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
        )
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    continents = models.IntegerField(choices=CONTINENT, default=0)
    content = models.TextField(max_length=4000, blank=True)
    excerpt = models.TextField(max_length=200, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    post_image = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    saved_post = models.ManyToManyField(
        User, related_name='post_saved', blank=True)

    class Meta:
        """
        Sorts the posts by date
        """
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns a string with the title of the post and
        name of author
        """
        return f"{self.title} | Written by {self.author}"
