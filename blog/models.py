from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True) #Спеціальне поля для слага, unique вказує,що вона не повторится

    def __str__(self): #Повертає строкове представлення об'єкта, тобто title
        return self.title

    #Робимо це, щоб в майбутньому джанго сам будував правильні формати посилань
    def get_absolute_url(self):
        #Першим аргументом передаємо назву маршрута. Потім передаємо словник, де ключ - аргумент який ми очікуємо в urls.py
        #А значення ключа ми беремо з цього об'єкта і в нього є атрибут slug
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категорія' #Те, як буде відображатись в адмінці слово в однині
        verbose_name_plural = 'Категорії'
        ordering = ['title'] #Вказуємо в якому порядку буде вестись сортування

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title'] #Вказуємо в якому порядку буде вестись сортування
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        #Першим аргументом передаємо назву маршрута. Потім передаємо словник, де ключ - аргумент який ми очікуємо в urls.py
        #А значення ключа ми беремо з цього об'єкта і в нього є атрибут slug
        return reverse('tag', kwargs={"slug": self.slug})

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубліковано')
    # upload_to - означає, що ми будем їх зберігати, blank - можуть бути пустими
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Кількість переглядів')
    #ForeignKey приймає силку на модель, з якую пов'язуємо
    #Якщо б Category була об'явлена пізніше цього класу, ми б мали заключити її в ''
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at'] #Вказуємо в якому порядку буде вестись сортування
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'

    def get_absolute_url(self):
        #Першим аргументом передаємо назву маршрута. Потім передаємо словник, де ключ - аргумент який ми очікуємо в urls.py
        #А значення ключа ми беремо з цього об'єкта і в нього є атрибут slug
        return reverse('post', kwargs={"slug": self.slug})