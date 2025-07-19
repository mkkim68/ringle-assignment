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
        fields = '__all__'


class UserMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    membership_type = MembershipTypeSerializer(read_only=True)

    class Meta:
        model = UserMembership
        fields = '__all__'

    is_active = serializers.SerializerMethodField()

    def get_is_active(self, obj):
        return obj.is_active()