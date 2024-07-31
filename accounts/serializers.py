from rest_framework import serializers
from django.contrib.auth.models import Group
from backoffice.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['date_joined']

class CreateUserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True)  # Accept group name as input

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'group']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_name = validated_data.pop('group')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return user