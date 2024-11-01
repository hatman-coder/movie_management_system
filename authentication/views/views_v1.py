from django.db.models import Q 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError, TokenBackendError
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.serializers_v1 import LoginSerializer, LogoutSerializer
from apps.user.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = str(user.id)
        token['name'] = str(user.get_full_name())
        token['username'] = str(user.username)

        data = dict()
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)

        return data


class LoginViewSet(ModelViewSet):
    model_class = User
    permission_classes = []

    def get_serializer_class(self):
        return LoginSerializer

    def create(self, request, *args, **kwargs):
        username_or_email = request.data.get('username_or_email', None)
        password = request.data.get('password', None)

        if not username_or_email or not password:
            return Response({'message': 'Username/Email and password is required'}, 406)

        user_obj = self.model_class.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

        if not user_obj:
            return Response({'message': 'Invalid username or email'}, 400)

        if not user_obj.is_active:
            return Response({'message': 'Your account is currently inactive. Please contact IT support for '
                                        'assistance.'}, 403)

        serializer_class = LoginSerializer
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            if user_obj.check_password(serializer.validated_data['password']):
                token = CustomTokenObtainPairSerializer.get_token(user_obj)
                token['message'] = 'Login successful'
                return Response(token, 202)
            else:
                return Response({'message': 'Invalid username or password'}, 400)
        else:
            return Response({'message': serializer.errors}, 400)


class LogoutViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        if 'refresh' not in request.data:
            return Response({'message': 'Token is required'}, 406)
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({"message": "Logout successful"}, 202)
        except (TokenError, TokenBackendError):
            return Response({"message": "Token is already blacklisted"}, 406)
