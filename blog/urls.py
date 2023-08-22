from django.urls import path

from .views import * #З views імпортуємо все

urlpatterns = [
    #path('', index, name='home'), #Так записуємо, коли використовуємо функції
    path('', Home.as_view(), name='home'), #Так записуємо, коли використовуємо клас
    #Не забуваємо про обов'язковий слеш в кінці
    #path('category/<str:slug>/', get_category, name='category'), #Django приймає в посилання або pk, або slug, потім передаємо функцію
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
]