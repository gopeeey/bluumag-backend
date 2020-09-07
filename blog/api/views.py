from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions, status
from blog.models import (
    Post,
    Category,
    Group,
    Rating,
    Quote,
    BodyImage,
    Tag,
    Image,
    Question,
    TrainingGroup
)
from .serializers import (
    PostSerializer,
    AddPostSerializer,
    EditPostSerializer,
    MiniPostSerializer,
    AddCategorySerializer,
    EditCategorySerializer,
    CategorySerializer,
    WriterCategorySerializer,
    MiniCategorySerializer,
    QuoteSerializer,
    SearchPostSerializer,
    WriterSearchPostSerializer,
    BodyImageSerializer,
    TagSerializer,
    ImageSerializer,
    EditImageSerializer,
    AddImageSerializer,
    QuestionSerializer,
    AddQuestionSerializer,
    TrainingGroupSerializer)
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.text import slugify
import functools
import operator
import json
from accounts.models import MyUser
from .permissions import IsWriter


class PostListView(ListAPIView,
                   APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ArticleList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, operation, group, category, page):
        if operation == 'home':
            featured = MiniPostSerializer(
                Post.objects.filter(featured=True).order_by('-id'), many=True, context={"request": request}).data
            homePosts = [{'name': 'featured', 'posts': featured}, ]
            categories = []

            for cat in Category.objects.all().order_by('id'):
                categories.append(Category.objects.get(name=cat))

            for cat in categories:
                posts = MiniPostSerializer(Post.objects.filter(category=cat).exclude(
                    featured=True).order_by('-id'), many=True, context={"request": request}).data
                if len(posts) > 7:
                    posts = posts[0:7]
                catPosts = {'name': cat.name, 'slug': cat.slug,
                            'groupSlug': cat.group.slug, 'main': cat.main, 'posts': posts}
                homePosts.append(catPosts)
            quotes = QuoteSerializer(Quote.objects.all(), many=True).data
            response = {'homePosts': homePosts, 'quotes': quotes}
            return Response(response, status=status.HTTP_200_OK)
        if operation == 'group':
            if group == 'favicon.ico':
                pass
            else:
                theGroup = Group.objects.get(slug=group)
                categories = Category.objects.filter(group=theGroup)
                groupPosts = []

                for cat in categories:
                    posts = MiniPostSerializer(Post.objects.filter(category=cat).order_by(
                        '-id'), many=True, context={"request": request}).data
                    if len(posts) > 7:
                        posts = posts[0:7]
                    catPosts = {'name': cat.name,
                                'slug': cat.slug,
                                'groupSlug': cat.group.slug,
                                'groupName': cat.group.name,
                                'groupDescription': cat.group.description,
                                'main': cat.main,
                                'posts': posts}
                    groupPosts.append(catPosts)
                return Response(groupPosts, status=status.HTTP_200_OK)
            return Response('', status=status.HTTP_204_NO_CONTENT)
        # this is a test
        # if operation == 'prerender':
        #     paramsList = []
        #     for group in Group.objects.all():
        #         paramsList.append(
        #             {"params": {
        #                 "groups": group.slug
        #             }}
        #         )
        #     return Response(paramsList, status=status.HTTP_200_OK)
        if operation == 'category':
            cat = Category.objects.get(slug=category)
            serialCat = CategorySerializer(
                cat, context={"request": request}).data
            allPosts = MiniPostSerializer(Post.objects.filter(category=cat).order_by(
                '-id'), many=True, context={"request": request}).data
            endPoint = int(page) * 10
            startPoint = (int(page) - 1) * 10
            length = len(allPosts)
            if length > endPoint:
                posts = allPosts[startPoint: endPoint]
            else:
                posts = allPosts[startPoint:]
            catPosts = {'name': serialCat["name"],
                        'groupSlug': serialCat["group"]["slug"],
                        'slug': serialCat["slug"],
                        'banner_xlarge': serialCat["banner_xlarge"],
                        'banner_large': serialCat["banner_large"],
                        'banner_nslarge': serialCat["banner_nslarge"],
                        'banner_normal': serialCat["banner_normal"],
                        'banner_medium': serialCat["banner_medium"],
                        'banner_small': serialCat["banner_small"],
                        'banner_xsmall': serialCat["banner_xsmall"],
                        'description': serialCat["description"],
                        'posts': posts,
                        'length': length}
            return Response(catPosts, status=status.HTTP_200_OK)

    def post(self, request, operation, group, category, page):
        allPosts = Post.objects.all().order_by('-id')
        position = request.POST.get("position")
        startPoint = (int(position) - 1) * 20
        endPoint = int(position) * 20
        length = len(allPosts)
        if length > endPoint:
            posts = allPosts[startPoint: endPoint]
        else:
            posts = allPosts[startPoint:]
        serialResult = WriterSearchPostSerializer(
            posts, many=True, context={"request": request}).data
        return Response({"total": length, "result": serialResult}, status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class QuotesList(ListAPIView,
                 APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class QuoteDetail(RetrieveAPIView,
                  APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


class QuoteDelete(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def get(self, request, id):
        try:
            Quote.objects.get(pk=id).delete()
            return Response('success', status=status.HTTP_200_OK)
        except:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class QuoteAdd(mixins.CreateModelMixin,
               generics.GenericAPIView,
               APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    queryset = Quote.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = QuoteSerializer

    def perform_create(self, serializer, request, *args, **kwargs):
        if (request.POST.get("edit") == "edit"):
            instance = Quote.objects.get(
                pk=int(request.POST.get("id")))
            newQuote = serializer.validated_data
            instance.body = newQuote["body"]
            instance.author = newQuote["author"]
            instance.save()

        else:
            instance = serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request, *args, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return Response('successful', status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class CategoriesList(ListAPIView,
                     APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    queryset = Category.objects.all()
    serializer_class = MiniCategorySerializer

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class CategoryDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        try:
            cat = WriterCategorySerializer(Category.objects.get(
                slug=slug), context={'request': request}).data
            return Response(cat, status=status.HTTP_200_OK)
        except:
            return Response('category does not exist', status=status.HTTP_404_NOT_FOUND)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class CategoryDelete(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def get(self, request, slug):
        try:
            Category.objects.filter(slug=slug).delete()
        except:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)
        return Response('success', status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class CategoryAdd(mixins.CreateModelMixin,
                  generics.GenericAPIView,
                  APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    queryset = Category.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddCategorySerializer

    def perform_create(self, serializer, request, *args, **kwargs):
        if (request.POST.get("edit") == "edit"):
            instance = Category.objects.get(
                slug=slugify(request.POST.get("name")))
            newCategory = serializer.validated_data
            instance.description = newCategory["description"]
            if not (type(request.POST.get("banner_xlarge")) is str):
                instance.banner_xlarge = newCategory["banner_xlarge"]
                instance.banner_large = newCategory["banner_large"]
                instance.banner_nslarge = newCategory["banner_nslarge"]
                instance.banner_normal = newCategory["banner_normal"]
                instance.banner_medium = newCategory["banner_medium"]
                instance.banner_small = newCategory["banner_small"]
                instance.banner_xsmall = newCategory["banner_xsmall"]
            instance.main = newCategory["main"]
            instance.group = Group.objects.get(
                slug=request.POST.get("group"))
            instance.save()

        else:

            instance = serializer.save(
                group=Group.objects.get(slug=request.POST.get("group")))

    def create(self, request, *args, **kwargs):
        if (type(request.POST.get("banner_xlarge")) is str) and (request.POST.get("edit") == "edit"):

            serializer = EditCategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request, *args, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return Response('successful', status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class ArticleDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, operation, slug):
        if operation == 'fetch':
            rawPost = Post.objects.get(slug=slug)
            related = rawPost.get_related()
            serialRelatedPosts = MiniPostSerializer(
                related, many=True, context={'request': request}).data
            post = PostSerializer(rawPost, context={"request": request}).data
            response = {"post": post, "related": serialRelatedPosts}
            return Response(response, status=status.HTTP_200_OK)
        if operation == 'prerender':
            paramsList = []
            for post in Post.objects.all():
                paramsList.append(
                    {"params": {
                        "slug": post.slug
                    }}
                )
            return Response([], status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class ViewsAdd(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            post = Post.objects.get(pk=int(id))
        except:
            return Response('not found', status=status.HTTP_404_NOT_FOUND)
        post.addView()
        return Response('success', status=status.HTTP_200_OK)


class RatingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id, review):
        post = Post.objects.get(pk=int(id))
        Rating.rate(post, int(review))
        return Response('successful', status=status.HTTP_202_ACCEPTED)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class Prerender(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, order):
        if order == 'appbar':
            groups = [{"name": g.name,
                       "slug": g.slug,
                       "categories": [{"name": c.name,
                                       "slug": c.slug,
                                       "groupSlug": c.group.slug} for c in g.category_set.all()]}
                      for g in Group.objects.all()]
            return Response(groups, status=status.HTTP_200_OK)
        if order == 'writer':
            categories = [{"name": c.name,
                           "slug": c.slug} for c in Category.objects.all()]
            return Response(categories, status=status.HTTP_200_OK)
        return Response("nothing", status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class Search(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        searchText = slugify(request.POST.get("searchText"))
        slugBits = ['-' + item + '-' for item in searchText.replace(
            '-a-', '-').replace('-an-', '-').split('-')]
        listRelName = functools.reduce(operator.add, (list(i) for i in (
            Post.objects.filter(searchSlug__contains=item) for item in slugBits)))
        unorderedRelatedID = [i.id for i in listRelName]
        orderedRelatedID = sorted(
            unorderedRelatedID, key=unorderedRelatedID.count, reverse=True)
        relatedID = list(dict.fromkeys(orderedRelatedID))
        result = []
        for item in relatedID:
            result.append(Post.objects.get(pk=item))
        if request.POST.get("user") == "writer":
            # posts.sort(key=lambda x: x.created_date, reverse=True)
            sortOption = request.POST.get("sort")
            sortOrder = request.POST.get("order")
            searchPage = request.POST.get("searchPage")
            endPoint = int(searchPage) * 20
            startPoint = (int(searchPage) - 1) * 20

            if sortOption == "relevance":
                if sortOrder == "ascending":
                    result.reverse()
                else:
                    pass
            elif sortOption == "name":
                if sortOrder == 'ascending':
                    result.sort(key=lambda x: x.title, reverse=False)
                else:
                    result.sort(key=lambda x: x.title, reverse=True)

            elif sortOption == "date":
                if sortOrder == 'ascending':
                    result.sort(key=lambda x: x.id, reverse=False)
                else:
                    result.sort(key=lambda x: x.id, reverse=True)
            elif sortOption == "views":
                if sortOrder == 'ascending':
                    result.sort(key=lambda x: x.views, reverse=False)
                else:
                    result.sort(key=lambda x: x.views, reverse=True)
            else:
                if sortOrder == 'ascending':
                    result.sort(
                        key=lambda x: x.rating.rating_index, reverse=False)
                else:
                    result.sort(
                        key=lambda x: x.rating.rating_index, reverse=True)

            length = len(result)
            if length > endPoint:
                posts = result[startPoint: endPoint]
            else:
                posts = result[startPoint:]
            serialResult = WriterSearchPostSerializer(
                posts, many=True, context={"request": request}).data
            return Response({"total": length, "result": serialResult}, status=status.HTTP_200_OK)
        serialResult = SearchPostSerializer(
            result, many=True, context={"request": request}).data
        return Response(serialResult, status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class DeletePost(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def get(self, request, id):
        try:
            Post.objects.filter(id=int(id)).delete()
        except:
            return Response('error', status=status.HTTP_417_EXPECTATION_FAILED)
        return Response('success', status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class FeaturedPosts(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def get(self, request):
        posts = Post.objects.filter(featured=True).order_by("-id")
        serial = WriterSearchPostSerializer(
            posts, many=True, context={"request": request}).data
        return Response(serial, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            instance = Post.objects.get(pk=int(request.POST.get("id")))
            instance.featured = False
            instance.save()
        except:
            return Response('error removing featured', status=status.HTTP_400_BAD_REQUEST)
        return Response('success', status=status.HTTP_200_OK)


class QuestionView(mixins.CreateModelMixin,
                   generics.GenericAPIView,
                   APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Question.objects.all()
    serializer_class = AddQuestionSerializer

    def perform_create(self, serializer, post, data):
        if data["edit"] == "edit":
            questionInstance = Question.objects.get(pk=int(data["id"]))
            newQuestion = serializer.validated_data
            questionInstance.question = newQuestion["question"]
            questionInstance.answer = newQuestion["answer"]
            questionInstance.save()
        else:
            serializer.save(post=post)

    def create(self, post, data, *args, **kwargs):
        serializer = AddQuestionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, post, data)
        return "done"

    def createquestion(self, post, data, *args, **kwargs):
        return self.create(post, data, *args, **kwargs)


class SlideImageView(mixins.CreateModelMixin,
                     generics.GenericAPIView,
                     APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer, id, data):
        try:
            post = Post.objects.get(pk=int(id))
        except:
            return "fetch error"
        if data["edit"] == "edit":
            slideInstance = Image.objects.get(pk=int(data["id"]))
            newSlide = serializer.validated_data
            if (data["image_xlarge"].name == "blob"):
                slideInstance.caption_title = newSlide["caption_title"]
                slideInstance.caption_body = newSlide["caption_body"]
                slideInstance.save()
            else:
                slideInstance.image_xlarge = newSlide["image_xlarge"]
                slideInstance.image_large = newSlide["image_large"]
                slideInstance.image_nslarge = newSlide["image_nslarge"]
                slideInstance.image_normal = newSlide["image_normal"]
                slideInstance.image_medium = newSlide["image_medium"]
                slideInstance.image_small = newSlide["image_small"]
                slideInstance.image_xsmall = newSlide["image_xsmall"]
                slideInstance.caption_title = newSlide["caption_title"]
                slideInstance.caption_body = newSlide["caption_body"]
                slideInstance.save()
        else:
            serializer.save(post=post)

    def create(self, id, request, *args, **kwargs):
        if (request.data.get("edit") == "edit") and (request.data.get("image_xlarge").name == "blob"):
            serializer = EditImageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        else:
            serializer = AddImageSerializer(data=request.data)
            if not (serializer.is_valid()):
                print(request.data)
            serializer.is_valid(raise_exception=True)

        state = self.perform_create(serializer, id, request.data)
        if state == "fetch error":
            return Response("error", status=status.HTTP_400_BAD_REQUEST)
        return Response("successful", status=status.HTTP_200_OK)

    # def createslide(self, post, data, *args, **kwargs):
    #     return self.create(post, data, *args, **kwargs)

    def post(self, request, id, *args, **kwargs):
        return self.create(id, request, *args, **kwargs)


class AddPost(mixins.CreateModelMixin,
              generics.GenericAPIView,
              APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AddPostSerializer

    def perform_create(self, serializer, request, *args, **kwargs):
        if (request.POST.get("edit") == "edit"):
            instance = Post.objects.get(
                slug=slugify(request.POST.get("title")))
            newPost = serializer.validated_data
            instance.description = newPost["description"]
            if not (type(request.POST.get("banner_xlarge")) is str):
                instance.banner_xlarge = newPost["banner_xlarge"]
                instance.banner_large = newPost["banner_large"]
                instance.banner_nslarge = newPost["banner_nslarge"]
                instance.banner_normal = newPost["banner_normal"]
                instance.banner_medium = newPost["banner_medium"]
                instance.banner_small = newPost["banner_small"]
                instance.banner_xsmall = newPost["banner_xsmall"]
            instance.body = newPost["body"]
            instance.featured = newPost["featured"]
            instance.writer = newPost["writer"]
            instance.category = Category.objects.get(
                slug=request.POST.get("category"))
            instance.save()
            newInstance = Post.objects.get(
                slug=slugify(request.POST.get("title")))
            serialInstance = PostSerializer(instance).data
            newSerialInstance = PostSerializer(newInstance).data
            existingTags = [i["name"] for i in serialInstance["tag_set"]]
            theList = json.loads(request.POST.get("tags"))
            newTags = [i["name"] for i in theList]
            for i in theList:
                if not (i["name"] in existingTags):
                    Tag.addTag(newInstance, i["name"])
            for i in existingTags:
                if not (i in newTags):
                    Tag.removeTag(newInstance, i)

            if request.POST.get("structure") == "interview":
                questions = request.POST.getlist("questions")
                answers = request.POST.getlist("answers")
                ids = request.POST.getlist("ids")
                edits = request.POST.getlist("edits")
                existingQuestions = [i["id"]
                                     for i in newSerialInstance["question_set"]]
                questionViewInstance = QuestionView()
                count = 0
                for i in existingQuestions:
                    if not (str(i) in ids):
                        Question.objects.filter(id=int(i)).delete()
                for i in questions:
                    data = {"question": i,
                            "answer": answers[count],
                            "id": ids[count],
                            "edit": edits[count]}
                    count = count + 1
                    QuestionView.createquestion(
                        questionViewInstance, post=instance, data=data, *args, **kwargs)
            return newInstance.id

        else:

            instance = serializer.save(category=Category.objects.get(
                slug=request.POST.get("category")))

            theList = json.loads(request.POST.get("tags"))
            for i in theList:
                Tag.addTag(instance, i["name"])

            if request.POST.get("structure") == "interview":
                questions = request.POST.getlist("questions")
                answers = request.POST.getlist("answers")
                edits = request.POST.getlist("edits")
                questionViewInstance = QuestionView()
                count = 0
                for i in questions:
                    data = {"question": i,
                            "answer": answers[count],
                            "edit": edits[count]}
                    count = count + 1
                    QuestionView.createquestion(
                        questionViewInstance, post=instance, data=data, *args, **kwargs)
            return instance.id

    def create(self, request, *args, **kwargs):
        if (type(request.POST.get("banner_xlarge")) is str) and (request.POST.get("edit") == "edit"):
            serializer = EditPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        postID = self.perform_create(serializer, request, *args, **kwargs)
        headers = self.get_success_headers(serializer.data)
        if (request.POST.get("structure") == "slide"):
            return Response({"message": "successful",
                             "post_id": postID}, status=status.HTTP_200_OK)
        return Response('successful', status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class BodyImageView(mixins.CreateModelMixin,
                    generics.GenericAPIView,
                    APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    queryset = BodyImage.objects.all()
    serializer_class = BodyImageSerializer

    def perform_create(self, serializer, request):
        instance = serializer.save()
        return instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_instance = self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        serializedImage = BodyImageSerializer(
            image_instance, context={"request": request}).data
        return Response({
            "urls": {
                "default": serializedImage["upload"],
                "600": serializedImage["upload_small"],
                "960": serializedImage["upload_medium"],
                "1280": serializedImage["upload_normal"],
                "1920": serializedImage["upload_nslarge"]
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class SearchTags(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def post(self, request):
        tagName = slugify(request.POST.get("tag_name"))
        serialTags = TagSerializer(Tag.objects.filter(
            slug__contains=tagName), many=True).data
        return Response(serialTags, status=status.HTTP_200_OK)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class TitleValidation(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def post(self, request, operation):
        if operation == "title":
            slug = slugify(request.POST.get("title"))
            try:
                instance = Post.objects.get(slug=slug)
            except:
                return Response("cool", status=status.HTTP_200_OK)
            return Response("exists", status=status.HTTP_226_IM_USED)
        if operation == "name":
            slug = slugify(request.POST.get("name"))
            try:
                instance = Category.objects.get(slug=slug)
            except:
                return Response("cool", status=status.HTTP_200_OK)
            return Response("exists", status=status.HTTP_226_IM_USED)

    def options(self, request):
        response = Response()
        response['headers'] = {
            # make sure you change all these access control urls before launch
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'applicaton/json'
        }
        return response


class WriterPostList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def post(self, request):
        sortOption = request.POST.get("sort")
        sortOrder = request.POST.get("order")
        position = request.POST.get("position")
        startPoint = (int(position) - 1) * 20
        endPoint = int(position) * 20
        if sortOption == "name":
            if sortOrder == 'ascending':
                allPosts = Post.objects.all().order_by('title')
            else:
                allPosts = Post.objects.all().order_by('-title')

        elif sortOption == "date":
            if sortOrder == 'ascending':
                allPosts = Post.objects.all().order_by('id')
            else:
                allPosts = Post.objects.all().order_by('-id')
        elif sortOption == "views":
            if sortOrder == 'ascending':
                allPosts = Post.objects.all().order_by('views')
            else:
                allPosts = Post.objects.all().order_by('-views')
        else:
            if sortOrder == 'ascending':
                ratings = Rating.objects.all().order_by(
                    'rating_index')
                allPosts = [i.post for i in ratings]
            else:
                ratings = Rating.objects.all().order_by(
                    '-rating_index')
                allPosts = [i.post for i in ratings]

        length = len(allPosts)
        if length > endPoint:
            posts = allPosts[startPoint: endPoint]
        else:
            posts = allPosts[startPoint:]
        serialResult = WriterSearchPostSerializer(
            posts, many=True, context={"request": request}).data
        return Response({"total": length, "result": serialResult}, status=status.HTTP_200_OK)


class TrainingGroupView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id, operation):
        if operation == "add":
            try:
                tGroup = TrainingGroup.objects.get(pk=int(id))
            except:
                return Response('group not found', status=status.HTTP_404_NOT_FOUND)
            tGroup.add_click()
            return Response('successful', status=status.HTTP_200_OK)

        if operation == 'list':
            tGroups = TrainingGroup.objects.all().order_by('id')
            serialTGroups = TrainingGroupSerializer(
                tGroups, many=True, context={"request": request}).data
            return Response(serialTGroups, status=status.HTTP_200_OK)
