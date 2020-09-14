from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.ItemList.as_view(), name='itemlist'),
    url(r'item/(?P<pk>\d+)/', views.ItemDetail.as_view(), name='itemdetail'),
    path('home/', views.StoreHomeView.as_view(), name="storehomeview")
]
