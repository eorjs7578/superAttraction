from django.urls import path
from . import views
from .views import profile_edit, profile_delete  # profile_edit 함수를 불러옵니다.

urlpatterns = [
    path('user/edit/', profile_edit, name='profile-edit'),  # 뷰 함수에 대한 URL 패턴을 수정합니다.
    path('user/delete/', profile_delete, name='profile-delete'),  # 뷰 함수에 대한 URL 패턴을 수정합니다.
    path('profile/<int:user_id>/', views.profileDetail),
]