# -*- coding: utf-8 -*-

# Create your views here.
from random import randint

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from rest.models import MarvelDatabase
from rest.serializers import MarvelSerializer


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
        total_count = MarvelDatabase.objects.count()
        limit, offset = 1, randint(1, total_count)
        random_marvel_character = MarvelDatabase.objects.all()[offset:offset+limit]
        if random_marvel_character.count() >= 1:
            return Response(
                MarvelSerializer(random_marvel_character[0]).data,
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_404_NOT_FOUND)
