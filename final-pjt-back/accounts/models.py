from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter

# 성별 선택 옵션
GENDER_CHOICES = [
    ('남성', '남성'),
    ('여성', '여성')
]

# 급여 선택 옵션
SALARY_CHOICES = [
    ('0~3000만원 미만', '0~3000만원 미만'),
    ('3000~6000만원 미만', '3000~6000만원 미만'),
    ('6000~1억미만', '6000~1억미만'),
    ('1억 이상', '1억 이상')
]



# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    salary = models.CharField(max_length=30, choices=SALARY_CHOICES)
    
    joinedProducts = models.ManyToManyField('financialProducts.DepositProducts', blank=True, related_name='User')
    
  
class CustomAccountAdapter(DefaultAccountAdapter):
  def save_user(self, request, user, form, commit=True):
    from allauth.account.utils import user_field, user_username
    data = form.cleaned_data
    username = data.get("username")
    # nickname 필드를 추가
    nickname = data.get("nickname")
    age = data.get("age")
    gender = data.get("gender")
    salary = data.get("salary")
    user_username(user, username)

    if nickname:
        user_field(user, "nickname", nickname)
    if age:
        user_field(user, "age", age)
    if gender:
        user_field(user, "gender", gender)
    if salary:
        user_field(user, "salary", salary)
    if "password1" in data:
        user.set_password(data["password1"])
    else:
        user.set_unusable_password()
    self.populate_username(request, user)
    if commit:
        # Ability not to commit makes it easier to derive from
        # this adapter by adding
        user.save()
    return user

class Profile(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    salary = models.CharField(max_length=100000, choices=SALARY_CHOICES)