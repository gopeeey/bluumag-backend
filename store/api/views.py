from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from store.models import (
    Item,
    Collection,
    Offer
)
from .serializers import (
    ItemSerializer,
    MiniCollectionSerializer,
    OfferSerializer

)


class ItemList(ListAPIView, APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetail(RetrieveAPIView, APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class StoreHomeView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        response = dict()
        featured_collections = Collection.objects.filter(homepage_banner=True)
        featured_offers = Offer.objects.filter(homepage_banner=True)
        if len(featured_collections) > 0:
            response['banner'] = MiniCollectionSerializer(
                featured_collections[0], context={'request': request}).data
        elif len(featured_offers) > 0:
            response['banner'] = OfferSerializer(
                featured_offers[0], context={'request': request}).data
        response['collections'] = MiniCollectionSerializer(
            Collection.objects.exclude(homepage_banner=True), many=True, context={'request': request}).data
        response['offers'] = OfferSerializer(Offer.objects.exclude(
            homepage_banner=True), many=True, context={'request': request}).data
        return Response(response, status=status.HTTP_200_OK)
