from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

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

