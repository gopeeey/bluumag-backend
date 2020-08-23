from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import MyUserSerializer, SimpleUserSerializer
from django.conf import settings
from .models import MyUser
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_verification_token
from django.urls import reverse


# Create your views here.


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = account_verification_token.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk)).decode()
                url = reverse('accountverificationview', kwargs={
                    'uidb64': uidb64,
                    'token': token
                })
                theresponse = {
                    'message': 'success',
                    'url': url
                }
                return Response(theresponse, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class UserDetail(APIView):

    def get(self, request):
        serialUser = SimpleUserSerializer(request.user).data
        return Response(serialUser, status=status.HTTP_200_OK)

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


class FormValidation(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, operation):
        if operation == 'email':
            try:
                theuser = MyUser.objects.get(email=request.POST.get('email'))
                if theuser:
                    return Response('taken', status=status.HTTP_226_IM_USED)
            except:
                return Response('go ahead', status=status.HTTP_202_ACCEPTED)

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


class AccountVerification(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        if user is not None and account_verification_token.check_token(user, token):
            user.verified = True
            user.is_active = True
            user.save()
            return Response('success', status=status.HTTP_200_OK)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
