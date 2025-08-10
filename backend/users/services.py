from django.contrib.auth import get_user_model
User = get_user_model()

def create_user(validated_data):
    """
    Service function to create a new user using validated data.
    """
    user = User.objects.create_user(
        username=validated_data["username"],
        email=validated_data["email"],
        password=validated_data["password"]
    )
    return user
