
from user.serializers import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


class login_view(APIView):
    def post(self, request):
        p = LoginSerializers(data=request.data)
        if p.is_valid():
            user = authenticate(
                request=request,
                username=request.data['username'],
                password=request.data['password'])

            if user:
                login(request, user)
                u = ShowLogin(request.data)
                r = {
                    'users': u.data
                }
                return Response(r)
            else:
                return Response({
                    'message': 'Username or password is wrong!!!'
                }, status=404)
        else:
            return Response({
                'errors': p.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class user_view(APIView):
    def post(self, request):
        s = addUserSerializer(data=request.data)
        if s.is_valid():
            s.save()
            r = {
                'message': 'successfully signed up!'
            }
            return Response(r)
        else:
            return Response({
                'errors': s.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'message': 'Send login request'
            }, status=401)
        else:
            p = updateUserSerializer(data=request.data, instance=request.user)
            if p.is_valid():
                p.save()
                return Response(
                    {
                        "message": "Your profile updated successfully"
                    }
                )
            else:
                return Response(
                    {
                        "errors": p.errors
                    }
                )

    def get(self, request):
        users = User.objects.all()
        s = UserSerializer(users, many=True)
        r = {
            'users': s.data
        }
        return Response(r)