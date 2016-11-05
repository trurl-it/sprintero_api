# -*- coding: utf -*-
from rest_framework import serializers

from rest.models import MarvelDatabase


class MarvelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarvelDatabase
        fields = [
            'id',
            'page_id',
            'name',
            'url_slug',
            'identity_status',
            'align',
            'eye_color',
            'hair_color',
            'sex',
            'gsm',
            'alive',
            'appearances',
            'first_appearance',
            'year',
        ]


class SlackDataSerializer(serializers.Serializer):
    token = serializers.CharField()
    team_id = serializers.CharField()
    team_domain = serializers.CharField()
    channel_id = serializers.CharField()
    channel_name = serializers.CharField()
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    command = serializers.CharField()
    text = serializers.CharField(required=False)
    response_url = serializers.CharField()
