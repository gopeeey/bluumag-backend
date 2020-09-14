from django.db import models
from django.conf import settings
from django.utils.text import slugify
from PIL import Image as PillowImage
from io import BytesIO
import sys
import functools
import operator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save


User = settings.AUTH_USER_MODEL

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    slug = models.SlugField(unique=True, default='',
                            blank=True, max_length=300)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    banner_xlarge = models.ImageField(upload_to='category_banners')
    banner_large = models.ImageField(upload_to='category_banners', blank=True)
    banner_nslarge = models.ImageField(
        upload_to='category_banners', blank=True)
    banner_normal = models.ImageField(upload_to='category_banners', blank=True)
    banner_medium = models.ImageField(upload_to='category_banners', blank=True)
    banner_small = models.ImageField(upload_to='category_banners', blank=True)
    banner_xsmall = models.ImageField(upload_to='category_banners', blank=True)
    created_date = models.DateField(auto_now_add=True)
    main = models.BooleanField(default=False)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None)
    slug = models.SlugField(unique=True,
                            blank=True, max_length=300)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    writer = models.CharField(max_length=100, default="Admin")
    banner_xlarge = models.ImageField(upload_to='banners')
    banner_large = models.ImageField(upload_to='banners', blank=True)
    banner_nslarge = models.ImageField(upload_to='banners', blank=True)
    banner_normal = models.ImageField(upload_to='banners', blank=True)
    banner_medium = models.ImageField(upload_to='banners', blank=True)
    banner_small = models.ImageField(upload_to='banners', blank=True)
    banner_xsmall = models.ImageField(upload_to='banners', blank=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default='')
    body = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    structure = models.CharField(max_length=15, default='')
    category = models.ForeignKey(
        Category, default=None, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True,
                            blank=True, max_length=500)
    searchSlug = models.SlugField(blank=True,  max_length=500)
    views = models.IntegerField(blank=True, default=0, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.searchSlug = '-' + slugify(self.title) + '-'

        super(Post, self).save(*args, **kwargs)

    def get_related(self):
        slugBits = ['-' + item + '-' for item in self.searchSlug.replace(
            '-is-', '-').replace('-a-', '-').replace('-an-', '-').replace('-was-', '-').split('-')]
        listRelName = functools.reduce(operator.add, (list(i) for i in (
            Post.objects.filter(searchSlug__contains=item) for item in slugBits)))
        shareTag = list(Post.objects.filter(tag__in=self.tag_set.all()))
        shareCat = list(Post.objects.filter(category=self.category))
        unorderedRelatedObj = listRelName + shareTag + shareCat
        unorderedRelatedID = [i.id for i in unorderedRelatedObj]
        orderedRelatedID = sorted(
            unorderedRelatedID, key=unorderedRelatedID.count, reverse=True)
        relatedID = list(dict.fromkeys(orderedRelatedID))
        relatedID.remove(self.id)
        related = []
        for item in relatedID:
            related.append(Post.objects.get(pk=item))
        if len(related) > 3:
            sliced = related[:3]
        else:
            sliced = related
        return sliced

    def addView(self):
        self.views = self.views + 1
        self.save()

    def __str__(self):
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image_xlarge = models.ImageField(upload_to='slides')
    image_large = models.ImageField(upload_to='slides', blank=True)
    image_nslarge = models.ImageField(
        upload_to='slides', blank=True)
    image_normal = models.ImageField(upload_to='slides', blank=True)
    image_medium = models.ImageField(upload_to='slides', blank=True)
    image_small = models.ImageField(upload_to='slides', blank=True)
    image_xsmall = models.ImageField(upload_to='slides', blank=True)
    caption_title = models.CharField(max_length=100)
    caption_body = models.TextField()

    def __str__(self):
        return self.post.title + ": " + self.caption_title


class Tag(models.Model):
    posts = models.ManyToManyField(Post)
    name = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, default='',
                            blank=True, max_length=300)

    @classmethod
    def addTag(cls, post, tag):
        currentTag, created = cls.objects.get_or_create(name=tag)
        currentTag.posts.add(post)

    @classmethod
    def removeTag(cls, post, tag):
        currentTag, created = cls.objects.get_or_create(name=tag)
        currentTag.posts.remove(post)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, primary_key=True)
    rating = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    total_reviews = models.IntegerField(default=0)
    rating_sum = models.IntegerField(default=0)
    rating_index = models.FloatField(default=0.0, null=True)

    def save(self, *args, **kwargs):
        self.rating_index = self.rating * self.rating_sum

        super(Rating, self).save(*args, **kwargs)

    @classmethod
    def rate(cls, post,  review):
        rating, created = cls.objects.get_or_create(post=post)
        rating.rating_sum += review
        rating.total_reviews += 1
        rating.rating = round(
            (float(rating.rating_sum) / float(rating.total_reviews)), 4)
        rating.save()

    def __str__(self):
        return self.post.title


def create_rating(sender, created, instance, **kwargs):
    if created:
        rating = Rating.objects.create(post=instance)


post_save.connect(create_rating, sender=Post)


class Quote(models.Model):
    body = models.TextField()
    author = models.CharField(max_length=500, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.body


class Question(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.TextField()
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + ": " + self.question


class BodyImage(models.Model):
    upload = models.ImageField(upload_to='bodyimages')
    upload_nslarge = models.ImageField(
        upload_to='bodyimages', blank=True)
    upload_normal = models.ImageField(upload_to='bodyimages', blank=True)
    upload_medium = models.ImageField(upload_to='bodyimages', blank=True)
    upload_small = models.ImageField(upload_to='bodyimages', blank=True)

    def save(self, *args, **kwargs):
        if ((not self.id) or (not (self.upload == BodyImage.objects.get(pk=self.id).upload))):
            self.upload = self.compressImage(self.upload, 2000)
            self.upload_nslarge = self.compressImage(self.upload, 1500)
            self.upload_normal = self.compressImage(self.upload, 1000)
            self.upload_medium = self.compressImage(self.upload, 750)
            self.upload_small = self.compressImage(self.upload, 500)

        super(BodyImage, self).save(*args, **kwargs)

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


class TrainingGroup(models.Model):
    name = models.CharField(max_length=20, default='New Group')
    link = models.TextField()
    clicks = models.IntegerField(default=0)

    def add_click(self):
        self.clicks = self.clicks + 1
        self.save()

    def __str__(self):
        return self.name
