from huggingface_hub import InferenceClient
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import MembershipType, User, UserMembership
from .serializers import UserMembershipSerializer

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'name': user.name
            }
        })

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
    
    user = User.objects.get(id=user_id)
    membership = MembershipType.objects.get(id=membership_id)

    if not user:
        return Response({'error': '유저를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    if not membership:
        return Response({'error': '멤버십을 찾을 수 없습니다'}, status=status.HTTP_404_NOT_FOUND)

    is_b2b_user = user.company is not None
    is_b2b_membership = membership.company is not None
    
    # if request.method == 'POST':
    #     user_membership = UserMembership.objects.create(
    #         user=user,
    #         membership_type=membership,
    #         end_date=timezone.now().date() + timedelta(days=membership.valid_days),
    #         remaining_conversations=membership.conversation_limit,
    #         remaining_analyses=membership.analysis_limit
    #     )
    #     print(user_membership.user)
    #     serializer = UserMembershipSerializer(user_membership)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # return Response({'error': '허용되지 않은 메서드입니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if is_b2b_membership:
        if not is_b2b_user or user.company != membership.company:
            return Response(
                {'error': '이 멤버십은 특정 회사 전용입니다. 유저 회사와 일치하지 않습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        if is_b2b_user:
            return Response(
                {'error': '이 멤버십은 개인용입니다. 회사 소속 유저에는 할당할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    user_membership = UserMembership.objects.create(
        user=user,
        membership_type=membership,
        end_date=timezone.now().date() + timedelta(days=membership.valid_days),
        remaining_conversations=membership.conversation_limit,
        remaining_analyses=membership.analysis_limit
    )
    
    serializer = UserMembershipSerializer(user_membership)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 유저가 멤버십 구매
@api_view(['POST'])
def purchase_membership(request):
    return

# 유저가 본인 멤버십 확인
@api_view(['GET'])
def get_my_membership(request):
    user = request.user
    
    if hasattr(user, 'membership'):
        serializer = UserMembershipSerializer(user.membership)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({
            'membership': None,
            'message': '현재 멤버십이 없습니다. 구매 후 이용해주세요.'
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def use_coupon(request):
    kind = request.data.get('kind')
    user = request.user
    membership = getattr(user, 'membership', None)

    if not membership:
        return Response({'error': '멤버십이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    if not membership.is_active():
        return Response({'error': '멤버십이 만료되었습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if kind == 'analysis':
        if membership.membership_type.analysis_limit == -1:
            return Response({'message': '무제한 멤버십입니다.'}, status=status.HTTP_200_OK)
        
        if membership.remaining_analyses <= 0:
            return Response({"error": '남은 분석 쿠폰이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        membership.remaining_analyses -= 1
        membership.save()

        return Response({
            'message': '분석 쿠폰이 차감되었습니다.',
            'remaining_analyses': membership.remaining_analyses
        }, status=status.HTTP_200_OK) 
    elif kind == 'conversation':
        if membership.membership_type.conversation_limit == -1:
            return Response({'message': '무제한 멤버십입니다.'}, status=status.HTTP_200_OK)
        
        if membership.remaining_conversations <= 0:
            return Response({"error": '남은 대화 쿠폰이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        membership.remaining_conversations -= 1
        membership.save()

        return Response({
            'message': '대화 쿠폰이 차감되었습니다.',
            'remaining_converstaions': membership.remaining_conversations
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def chat_with_ai(request):
    user_message = request.data.get('message', '')
    if not user_message:
        return Response({'error': '메시지가 비어있습니다.'}, status=400)

    try:
        client = InferenceClient(
            api_key=settings.HF_API_TOKEN,
            provider="hf-inference"
        )

        completion = client.chat.completions.create(
            model="HuggingFaceTB/SmolLM3-3B",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )

        full_text = completion.choices[0].message.content
        if "</think>" in full_text:
            response_text = full_text.split("</think>")[-1].strip()
        else:
            response_text = full_text.strip()

        return Response({'response': response_text}, status=200)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=500)