"""Request/response serializers for auth and profile endpoints."""

from __future__ import annotations

from rest_framework import serializers

from .models import Device, Language, Platform, User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "name",
            "avatar_url",
            "city",
            "city_name",
            "about",
            "language",
            "show_phone",
            "role",
            "is_verified",
            "rating_avg",
            "rating_count",
            "date_joined",
        )
        read_only_fields = fields

    def get_avatar_url(self, obj: User) -> str | None:
        return obj.avatar.url if obj.avatar else None

    def get_city_name(self, obj: User) -> str | None:
        return obj.city.name_uz if obj.city else None


class SmsSendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class SmsSendResponseSerializer(serializers.Serializer):
    phone = serializers.CharField()
    resend_after_seconds = serializers.IntegerField()


class DeviceMetaSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=Platform.choices, required=False, allow_blank=True)
    app_version = serializers.CharField(required=False, allow_blank=True, max_length=20)


class SmsVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6, min_length=6)
    device = DeviceMetaSerializer(required=False)


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    is_new = serializers.BooleanField()
    user = UserSerializer()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ProfileUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=40)
    about = serializers.CharField(required=False, allow_blank=True, max_length=200)
    language = serializers.ChoiceField(choices=Language.choices, required=False)
    city_id = serializers.IntegerField(required=False)
    show_phone = serializers.BooleanField(required=False)


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("fcm_token", "platform", "app_version")


class DeleteAccountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
