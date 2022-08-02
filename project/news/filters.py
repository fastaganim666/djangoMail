from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {

           'text': ['icontains'],
           'name': ['icontains'],
           'time_add': [
               'lt',
               'gt',
           ],
       }