from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {  # type: ignore
            "id": self.user.id,  # type: ignore
            "username": self.user.username,  # type: ignore
        }

        return data
