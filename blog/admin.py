from django.contrib import admin
from .models import (
    Post,
    Category,
    Image,
    Group,
    Tag,
    Rating,
    Quote,
    Question
)

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Group)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Quote)
admin.site.register(Question)
