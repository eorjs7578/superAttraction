# accounts/serializers.py
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User, GENDER_CHOICES, SALARY_CHOICES
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from .models import Profile
from financialProducts.models import DepositProducts
UserModel = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
 # 필요한 필드들을 추가합니다.
 nickname = serializers.CharField(
 required=False,
 allow_blank=True,
 max_length=255
 )
 age = serializers.CharField(required=False, max_length=20)
 gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False,)
 salary = serializers.ChoiceField(choices=SALARY_CHOICES, required=False,)
 # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
 def get_cleaned_data(self):
    return {
      'username': self.validated_data.get('username', ''),
      'password1': self.validated_data.get('password1', ''),
      'nickname': self.validated_data.get('nickname', ''),
      'age': self.validated_data.get('age', ''),
      'gender': self.validated_data.get('gender', ''),
      'salary': self.validated_data.get('salary', ''),
    }

class CustomUserDetailsSerializer(UserDetailsSerializer):
 class Meta:
    extra_fields = []
    # see https://github.com/iMerica/dj-rest-auth/issues/181
    # UserModel.XYZ causing attribute error while importing other
    # classes from `serializers.py`. So, we need to check whether the auth model has
    # the attribute or not
    if hasattr(UserModel, 'USERNAME_FIELD'):
        extra_fields.append(UserModel.USERNAME_FIELD)
    if hasattr(UserModel, 'nickname'):
        extra_fields.append('nickname')  
    if hasattr(UserModel, 'age'):
        extra_fields.append('age')
    if hasattr(UserModel, 'gender'):
        extra_fields.append('gender')
    if hasattr(UserModel, 'salary'):
        extra_fields.append('salary')
    model = UserModel
    fields = ('pk', *extra_fields)
    read_only_fields = ('email',)

class ProfileSerializer(serializers.ModelSerializer):
    class DepositProductsSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositProducts
            fields = '__all__'
    joinedProducts = DepositProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'