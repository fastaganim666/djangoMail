from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'AT'
    news = 'NS'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POSITIONS, default=news)
    time_add = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    many_to_many_relation = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return f'{self.text[0:124]}...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_add = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
