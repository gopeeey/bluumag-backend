from django.contrib import admin
from .models import (
    Category,
    SubCategory,
    SubCategoryClass,
    Item,
    ItemVariant,
    Image,
    Specification,
    Collection,
    Offer
)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubCategoryClass)
admin.site.register(Item)
admin.site.register(ItemVariant)
admin.site.register(Image)
admin.site.register(Specification)
admin.site.register(Collection)
admin.site.register(Offer)

# Register your models here.
