from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from django.db.models import F

class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts' #Так буде називатись наш об'єкт з постами
    paginate_by = 4 #Вказуємо, скільки постів буде на 1 сторінці пагінації

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'
        return context

class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False #При запиті неіснуючої категорії буде 404

    def get_queryset(self):
        #Ми беремо пости через фільтр, категорія яких дорівнює нашому слагу
        #Тобто ми звертаємося до поля category моделі Post, а slug беремо вже з відповідної моделі Category
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        #Ми беремо пости через фільтр, категорія яких дорівнює нашому слагу
        #Тобто ми звертаємося до поля category моделі Post, а slug беремо вже з відповідної моделі Category
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug'])) #Приводимо Tag в троку
        return context

class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1 #Міняємо кількість переглядів
        self.object.save()
        self.object.refresh_from_db() #Перезапитуємо дані з бд
        return context

class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # Шукаємо, щоб тайтл був такий, як в запиті. В кирилиці важливий регістр
        # ICONTAINS не зважає на регістр, але це працює тільки з латиницею
        # Забираємо з реквеста,тобто з нашого запиту. GET - це масив, а get() це фукнція, яка вже забирає з масиву
        return Post.objects.filter(title__icontains=self.request.GET.get('s')) #'s' - це назва нашого запиту в single.html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #Додаємо це, щоб зробити можливим пагінацію
        context['s'] = f"s={self.request.GET.get('s')}&" #Тобто перший get-параметр буде self...('s'), далі & і номер сторінки
        return context
