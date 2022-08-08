from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from .models import SubscribersCategory


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       your_name = forms.CharField(label='Your name', max_length=100)
       fields = [
           'name',
           'text',
           'author',
           'categories'
       ]

       def clean(self):
           cleaned_data = super().clean()
           text = cleaned_data.get("text")
           if text is not None and len(text) < 20:
               raise ValidationError({
                   "text": "Описание не может быть менее 20 символов."
               })

           name = cleaned_data.get("name")
           if name == text:
               raise ValidationError(
                   "Текст и название не должны быть идентичны!"
               )

           return cleaned_data

class SubscribeForm(forms.ModelForm):
   class Meta:
       model = SubscribersCategory
       fields = [
           'category',
       ]
