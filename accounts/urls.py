from django.urls import path
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(),
         name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', views.UserCreate.as_view(), name='usercreate_view'),
    path('user/detail/', views.UserDetail.as_view(), name='userdetail_view'),
    url(r'^formvalidation/(?P<operation>.+)/$',
        views.FormValidation.as_view(), name='formvalidationview'),
    url(r'^verification/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.AccountVerification.as_view(), name='accountverificationview')
]
