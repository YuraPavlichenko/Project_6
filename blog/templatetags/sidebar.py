#Тут будуть теги для сайт бара

from django import template
from blog.models import Post, Tag

register = template.Library()

@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):
    # Отримуємо пости в оберненому порядку сортування по views, а також регулюємо їх кількість  зрізом
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}

@register.inclusion_tag('blog/tags_tpl.html')
def get_tags():
    tags = Tag.objects.all()
    return {"tags": tags}
