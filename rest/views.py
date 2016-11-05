# -*- coding: utf-8 -*-

# Create your views here.
import json
from random import randint
from urlparse import urljoin

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView

from rest.models import MarvelDatabase
from rest.serializers import MarvelSerializer, SlackDataSerializer

from django.conf import settings


def get_random_character(badass=False):

    if not badass:
        queryset = MarvelDatabase.objects.filter(align='Good Characters')
    else:
        queryset = MarvelDatabase.objects.filter(align='Bad Characters')
    total_count = queryset.count()
    limit, offset = 1, randint(1, total_count)
    return queryset.all()[offset:offset + limit]


class MarvelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = MarvelDatabase.objects.all()
    serializer_class = MarvelSerializer

    @list_route(methods=['get'])
    def generate(self, request, *args, **kwargs):
        # this should be bulletproof -> basically do not use id;
        # use offset and limit;
        print(dir(request))
        random_marvel_character = get_random_character(badass=request.query_params.get('badass', False))
        if random_marvel_character.count() >= 1:
            return Response(
                MarvelSerializer(random_marvel_character[0]).data,
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_404_NOT_FOUND)


class SlackPOSTView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = SlackDataSerializer(data=request.query_params)
        if not serializer.is_valid():
            Response(status=status.HTTP_400_BAD_REQUEST)
        # check token
        if serializer.data.get('token') != settings.SLACK_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # check command - only one supported now
        if serializer.data.get('command') not in settings.SUPPORTED_SLACK_COMMANDS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if 'wellknown' in serializer.data.get('text', []):
            # add support for well known characters;
            pass

        badass = False
        if 'badass' in serializer.data.get('text', []):
            # add support for badass characters;
            badass = True

        random_marvel_character = get_random_character(badass)
        if random_marvel_character.count() >= 1:
            serialized_data = MarvelSerializer(random_marvel_character[0]).data
            name = serialized_data['name'].replace('(Earth-616)', '').strip()
            url = urljoin(settings.MARVEL_WIKIA, serialized_data['url_slug'].replace('\\', ''))
            data = {
                "attachments": [
                    {
                        "fallback": name,
                        "pretext": "Sprintero gives you names",
                        "title": name,
                        "title_link": url,
                        "text": "Character is {}. And is in the {} group.".format(
                            "still_alive" if serialized_data["alive"] == "Living Characters" else "dead",
                            serialized_data["align"],
                        ),
                        "color": "#7CD197"
                    }
                ]
            }
            return Response(
                json.dumps(data),
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

