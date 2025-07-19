from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import MembershipType, User, UserMembership
from .serializers import UserMembershipSerializer, CompanySerializer, UserSerializer, MembershipTypeSerializer

# 멤버십 생성
@api_view(['POST'])
def create_membership(request):
    if request.method == 'POST':
        serializer = MembershipTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 멤버십 삭제
@api_view(['DELETE'])
def delete_membership(request, membership_pk):
    membership = get_object_or_404(MembershipType, pk=membership_pk)
    if request.method == 'DELETE':
        my_dict = {'delete': f'멤버십 {membership_pk}을/를 삭제했습니다.'}
        membership.delete()
        return Response(my_dict)
    return Response({'error': '허용되지 않은 메서드입니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 관리자가 멤버십 직접 할당
@api_view(['POST'])
def assign_membership(request):
    user_id = request.data.get('user_id')
    membership_id = request.data.get('membership_id')
    
    user_qs = User.objects.filter(id=user_id)
    membership_qs = MembershipType.objects.filter(id=membership_id)
    if not user_qs.exists():
        return Response({'error': '유저를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    if not membership_qs.exists():
        return Response({'error': '멤버십을 찾을 수 없습니다'}, status=status.HTTP_404_NOT_FOUND)
    
    user = user_qs.first()
    membership = membership_qs.first()
    
    if request.method == 'POST':
        user_membership = UserMembership.objects.create(
            user=user,
            membership_type=membership,
            end_date=timezone.now().date() + timedelta(days=membership.valid_days),
            remaining_conversations=membership.conversation_limit,
            remaining_analyses=membership.analysis_limit
        )
        serializer = UserMembershipSerializer(user_membership)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({'error': '허용되지 않은 메서드입니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# 유저가 멤버십 구매
@api_view(['POST'])
def purchase_membership(request):
    return

# 유저가 본인 멤버십 확인
@api_view(['GET'])
def get_my_membership(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    
    if hasattr(user, 'membership'):
        serializer = UserMembershipSerializer(user.membership)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'membership': None,
            'message': '현재 멤버십이 없습니다. 구매 후 이용해주세요.'
        }, status=status.HTTP_200_OK)