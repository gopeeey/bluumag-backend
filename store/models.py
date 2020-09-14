from django.db import models
from django.utils.text import slugify
from PIL import Image as PillowImage
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True,
                            blank=True, max_length=300)
    description = models.CharField(max_length=2000)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=False,
                            blank=True, max_length=300)
    description = models.CharField(max_length=2000)
    created_date = models.DateField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.category.name + ": " + self.name


class SubCategoryClass(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=False,
                            blank=True, max_length=300)
    description = models.CharField(max_length=2000)
    created_date = models.DateField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, default=None)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(SubCategoryClass, self).save(*args, **kwargs)

    def __str__(self):
        return self.category.name + ": " + self.subcategory.name + ": " + self.name


class Item(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=2000)
    item_type = models.CharField(max_length=30, default="other")
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    badge = models.CharField(max_length=50)
    video = models.FileField(upload_to="videos", blank=True)
    subcategory_classes = models.ManyToManyField(SubCategoryClass)
    subcategories = models.ManyToManyField(SubCategory)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True,
                            blank=True, max_length=300)

    def save(self, *args, **kwargs):
        if self.id:
            self.slug = slugify(self.name + "-" + str(self.id))
        else:
            if Item.objects.count() == 0:
                self.slug = slugify(self.name + "-1")
            else:
                self.slug = slugify(
                    self.name + "-" + str(Item.objects.last().id + 1))

        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=300)
    items = models.ManyToManyField(Item, default=None)
    created_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    homepage_banner = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(blank=True, max_length=300)
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    subcategory = models.OneToOneField(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    item = models.OneToOneField(
        Item, on_delete=models.CASCADE, blank=True, null=True)
    collection = models.OneToOneField(
        Collection, on_delete=models.CASCADE, blank=True, null=True)
    homepage_banner = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.category:
            self.slug = slugify(self.category.slug)
        elif self.subcategory:
            self.slug = slugify(self.subcategory.slug)
        elif self.collection:
            self.slug = slugify(self.collection.slug)
        else:
            self.slug = slugify(self.item.slug)

        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ItemVariant(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="variants", default=None)
    name = models.CharField(max_length=100)
    in_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.item.name + " " + self.name


class Specification(models.Model):
    shoe_size = models.IntegerField(blank=True, null=True)
    clothing_size = models.CharField(max_length=40, blank=True, null=True)
    item_variant = models.ForeignKey(
        ItemVariant, related_name="specifications", on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="specifications_list", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.item = self.item_variant.item

        super(Specification, self).save(*args, **kwargs)

    def __str__(self):
        return self.item_variant.item.name + " " + self.item_variant.name + " " + "specs" + " " + str(self.id)


class Image(models.Model):
    image_xlarge = models.ImageField(upload_to='store_images')
    image_large = models.ImageField(upload_to='store_images', blank=True)
    image_nslarge = models.ImageField(upload_to='store_images', blank=True)
    image_normal = models.ImageField(upload_to='store_images', blank=True)
    image_medium = models.ImageField(upload_to='store_images', blank=True)
    image_small = models.ImageField(upload_to='store_images', blank=True)
    image_xsmall = models.ImageField(upload_to='store_images', blank=True)
    caption = models.TextField(blank=True)
    item_variant = models.ForeignKey(
        ItemVariant, related_name="images", on_delete=models.CASCADE,
        blank=True, default=None, null=True)
    subcategory = models.OneToOneField(
        SubCategory, related_name="banner_image", on_delete=models.CASCADE,
        blank=True, default=None, null=True)
    collection = models.OneToOneField(
        Collection, related_name="image", on_delete=models.CASCADE,
        blank=True, default=None, null=True)
    offer = models.OneToOneField(
        Offer, related_name="image", on_delete=models.CASCADE,
        blank=True, default=None, null=True)

    def save(self, *args, **kwargs):
        if ((not self.id) or (not (self.image_xlarge == Image.objects.get(pk=self.id).image_xlarge))):
            self.image_xlarge = self.compressImage(self.image_xlarge, 2500)
            self.image_large = self.compressImage(self.image_xlarge, 2000)
            self.image_nslarge = self.compressImage(self.image_xlarge, 1500)
            self.image_normal = self.compressImage(self.image_xlarge, 1000)
            self.image_medium = self.compressImage(self.image_xlarge, 750)
            self.image_small = self.compressImage(self.image_xlarge, 500)
            self.image_xsmall = self.compressImage(self.image_xlarge, 300)

        super(Image, self).save(*args, **kwargs)

    def compressImage(self, image, width):
        imageTemp = PillowImage.open(image)
        imageTemp = imageTemp.convert('RGB')
        imageWidth = float(imageTemp.size[0])
        outputIoStream = BytesIO()
        if int(imageWidth) <= width:
            imageTemp.save(outputIoStream, format='JPEG', quality=65)
            outputIoStream.seek(0)
            image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split(
                '.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
            return image
        widthPercent = (float(width)/imageWidth)
        height = int(float(imageTemp.size[1]) * widthPercent)
        imageTemp = imageTemp.resize(
            (width, height), PillowImage.ANTIALIAS)
        imageTemp.save(outputIoStream, format='JPEG', quality=65)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split(
            '.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image

    def __str__(self):
        if self.subcategory:
            return self.subcategory.name + " category banner image"
        elif self.item_variant:
            return self.item_variant.item.name + " " + self.item_variant.name + " image"
        elif self.collection:
            return self.collection.name + " Collection Image"
        elif self.offer:
            return self.offer.title + " Offer Image"
        else:
            return self.caption
