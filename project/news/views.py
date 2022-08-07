from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, reverse, redirect

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post, SubscribersCategory


def notify_managers_appointment(sender, instance, created, **kwargs):
    subject = f'{instance.name} {instance.text}'

    mail_managers(
        subject=instance.name,
        message=instance.text,
    )

post_save.connect(notify_managers_appointment, sender=Post)




class PostsList(ListView):
    model = Post
    ordering = 'name'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):
        post = Post(
            name=request.POST['name'],
            text=request.POST['text'],
            author_id=request.POST['author']
        )
        post.save()

        name = request.POST['name']
        text = request.POST['text']
        text = text[0:50] + '...'
        p = Post.objects.filter(type='AT').values('text')
        p = list(p)

        send_mail(
            subject=f'{p} ee',
            message=f'{p}',
            from_email='fastaganim666@yandex.ru',
            recipient_list=['fastaganim666@gmail.com']
        )
        return redirect('/posts/')

class Subscribe(PermissionRequiredMixin, CreateView):
    form_class = SubscribeForm
    model = SubscribersCategory
    template_name = 'subscribe.html'
    permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):
        subscribe = SubscribersCategory(
            category_id=request.POST['category'],
            user_id=request.user.id,
        )
        subscribe.save()

        return redirect('/posts/')




class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')