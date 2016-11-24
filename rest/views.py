# -*- coding: utf-8 -*-

from random import randint

import requests
from django.shortcuts import redirect
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView

from core.views import success_view
from rest.helpers import to_bool
from rest.models import MarvelDatabase
from rest.serializers import MarvelSerializer, SlackDataSerializer

from django.conf import settings

from rest.slack_formatting import SlackFormatter


def get_random_character(badass=False, wellknown=False):

    if not badass:
        queryset = MarvelDatabase.objects.filter(align='Good Characters')
    else:
        queryset = MarvelDatabase.objects.filter(align='Bad Characters')
    if wellknown:
        queryset = queryset.filter(is_well_known=True)
    total_count = queryset.count()

    limit, offset = 1, randint(0, total_count-1)
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

        random_marvel_character = get_random_character(
            badass=to_bool(request.query_params.get('badass', False)),
            wellknown=to_bool(request.query_params.get('wellknown', False)),
        )
        if random_marvel_character.count() >= 1:
            return Response(
                MarvelSerializer(random_marvel_character[0]).data,
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_404_NOT_FOUND)


class SlackPOSTView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SlackDataSerializer(data=request.data)
        if not serializer.is_valid():
            Response(status=status.HTTP_400_BAD_REQUEST)
        # check token
        if serializer.data.get('token') != settings.SLACK_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # check command - only one supported now
        if serializer.data.get('command') not in settings.SUPPORTED_SLACK_COMMANDS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        command_text = serializer.data.get('text', [])

        if 'help' in command_text:
            return Response(
                {
                    "text": "To use sprintero write (it generates for you sprint names):\n"
                            "/sprintero - will give you good character name from over 8k names in database\n"
                            "/sprintero wellknown - will give you wellknown and good character name\n"
                            "/sprintero badass - will give you bad character name\n"
                            "/sprintero wellknown badass - will give you a well known bad character name\n"
                },
                status=status.HTTP_200_OK
            )

        wellknown = False
        if 'wellknown' in command_text:
            wellknown = True

        badass = False
        if 'badass' in command_text:
            # add support for badass characters;
            badass = True

        random_marvel_character = get_random_character(badass, wellknown)
        if random_marvel_character.count() >= 1:
            serialized_data = MarvelSerializer(random_marvel_character[0]).data
            data = SlackFormatter().format(serialized_data)
            return Response(
                data,
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_404_NOT_FOUND)


class SlackOauthView(APIView):

    def get(self, request, *args, **kwargs):
        data = {
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_SECRET,
            'code': request.query_params.get('code')
        }

        response = requests.post('https://slack.com/api/oauth.access', data=data)
        json_response = response.json()
        if response.status_code == status.HTTP_200_OK and json_response['ok']:
            token = response.json().get('access_token')
            # ask about team name:
            response = requests.post('https://slack.com/api/team.info', data={
                'token': token
            })
            json_response = response.json()
            if json_response:
                team_domain = json_response.get('team', {}).get('domain')
                if team_domain:
                    return redirect(success_view, team_domain)

        return Response(status=status.HTTP_400_BAD_REQUEST)
