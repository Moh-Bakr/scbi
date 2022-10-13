from rest_framework.decorators import api_view
from .utilities.RefreshToken import get_tokens_for_user
from rest_framework.response import  Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from .serializers.RegistrationSerializer import RegistrationSerializer


@api_view(['POST'])
def Register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
    #   return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response({'msg': 'User Created '}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def Login(request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
