from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer
from .models import User
from django.shortcuts import get_object_or_404
from .serializers import CustomUserDetailsSerializer


UserModel = get_user_model()

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_edit(request):
    user = request.user
    serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)  # partial=True를 통해 부분 업데이트 허용
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request):
    try:
        # 현재 로그인한 사용자를 가져옵니다.
        user = request.user
        # 사용자 계정을 삭제합니다.
        user.delete()
        # 성공적으로 삭제되었음을 알리는 응답을 반환합니다.
        return Response({'message': 'Your account has been successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    except:
        # 예외가 발생할 경우, 오류 메시지를 반환합니다.
        return Response({'error': 'Something went wrong when trying to delete the account.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def profileDetail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = ProfileSerializer(user)
    return Response(serializer.data)    