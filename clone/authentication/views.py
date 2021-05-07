from django.shortcuts import render
import json
from rest_framework import permissions, status, viewsets, views
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout

from .models import User
from .serializers import UserSerializer
from .permissions import  IsUser

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated, IsUser(),)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        
        return Response(
            {
                'status': 'Bad request',
                'message': "User could not be created with recieved data",
            }, 
        status.HTTP_400_BAD_REQUEST)



class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = json.loads(request.body)
        print(data)

        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)

                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(
                    {'status': 'Unauthorized', 'message': 'This user has been disabled'}, 
                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'Unauthorized', 'message': 'Username or password combination invalid'}, 
                status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

