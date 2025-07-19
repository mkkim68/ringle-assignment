from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import MembershipType, User
from .serializers import UserMembershipSerializer, CompanySerializer, UserSerializer, MembershipTypeSerializer

@api_view(['POST'])
def create_membership(request):
    if request.method == 'POST':
        serializer = MembershipTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_membership(request, membership_pk):
    membership = get_object_or_404(MembershipType, pk=membership_pk)
    if request.method == 'DELETE':
        my_dict = {'delete': f'멤버십 {membership_pk}을/를 삭제했습니다.'}
        membership.delete()
        return Response(my_dict)
    return Response({'error': '허용되지 않은 메서드입니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def assign_membership(request):
    return

@api_view(['POST'])
def purchase_membership(request):
    return

@api_view(['GET'])
def get_my_membership(request):
    return