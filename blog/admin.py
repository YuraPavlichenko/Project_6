from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    #Цей параметр буде переводити наш title в slug автоматично. Тобто, title puki kaki 12 буде переведено в puki_kaki_12
    prepopulated_fields = {"slug": ("title",)} #Після title ставимо кому бо це кортеж і в ньому всього 1 елемент
    form = PostAdminForm
    #save_as = True #Дає нам можливість відкрити пост і створити такий самий пост з вже заповненими полями

    save_on_top = True #Щоб набір кнопок був також і зверху, а не тільки знизу

    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'get_photo', 'views') #Вказуємо, які поля будуть відображатися в адмінці

    list_display_links = ('id', 'title') #Робимо ці поля ссилками
    search_fields = ('title',) #Можемо шукати за цим полем
    list_filter = ('category', 'tags') #Відбираємо пости тільки необзідних категорій
    readonly_fields = ('views', 'created_at', 'get_photo') #Можемо тільки читати ці поля
    # Поля, які ми показуємо в самому тілі поста
    fields = ('title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at')

    #Відображамо фото не як строку, а я фото в адмінці
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'фото' #Щоб в адмінці писало photo, а не get_photo

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

#Реєструємо наші моделі
admin.site.register(Category, CategoryAdmin) #Добавляємо наші класи, щоб вони відпрацьовували
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)