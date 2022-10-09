from rest_framework import serializers
from ..models import CustomUser
from rest_framework.response import Response
from rest_framework import status
import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class RegistrationSerializer(serializers.ModelSerializer):
    password_conform = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',
                  'password', 'password_conform']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomUser(email=self.validated_data['email'], first_name=self.validated_data['first_name'],
                          last_name=self.validated_data['last_name'])
        password = self.validated_data['password']
        
        errors = dict()
        try:
             validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
        if errors:
             raise serializers.ValidationError(errors)
        

        password_conform = self.validated_data['password_conform']
        if password != password_conform:
            raise serializers.ValidationError(
                {'msg': 'password and conformation password must match.'})
        user.set_password(password)

        user.save()
        return user
