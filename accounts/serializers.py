from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from backoffice.models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajoutez des informations supplémentaires
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        # Ajoutez les groupes de l'utilisateur
        groups = user.groups.all()
        token['group'] = groups[0].name if groups else None

        return token


# Sérializer pour les utilisateurs
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['date_joined']

# Sérializer pour créer un utilisateur avec un groupe
class CreateUserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True)  # Accepter le nom du groupe en entrée

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

# Sérializer pour l'enregistrement
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.is_active = False  # L'utilisateur doit valider son compte
        user.save()
        return user

# Sérializer pour la connexion
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('Both username and password are required')

        return data


# Sérializer pour la demande de réinitialisation de mot de passe
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return user

# Sérializer pour confirmer la réinitialisation de mot de passe
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
