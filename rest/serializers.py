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
