from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from typing import Any, Dict


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        data['success'] = True
        data['user'] = self.user.username

        data.pop('refresh', None)
        data.pop('access', None)

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
