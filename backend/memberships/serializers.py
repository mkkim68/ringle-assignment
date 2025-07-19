from rest_framework import serializers
from .models import Company, User, MembershipType, UserMembership


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'company']


class MembershipTypeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = MembershipType
        fields = ['id', 'name', 'valid_days', 'conversation_limit', 'analysis_limit', 'company']


class UserMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    membership_type = MembershipTypeSerializer(read_only=True)

    class Meta:
        model = UserMembership
        fields = [
            'id',
            'user',
            'membership_type',
            'start_date',
            'end_date',
            'remaining_conversations',
            'remaining_analyses',
            'is_active',
        ]

    is_active = serializers.SerializerMethodField()

    def get_is_active(self, obj):
        return obj.is_active()