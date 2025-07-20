from datetime import timedelta
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
    end_date = serializers.SerializerMethodField()

    def get_is_active(self, obj):
        return obj.is_active()
    
    def get_end_date(self, obj):
        return obj.end_date or (
            obj.start_date + timedelta(days=obj.membership_type.valid_days)
            if obj.start_date and obj.membership_type else None
        )

