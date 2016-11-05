# -*- coding: utf-8 -*-
"""sprintero_api URL Configuration"""

from django.conf.urls import url, include

from rest.views import SlackPOSTView

urlpatterns = [
     url(r'^sprintero/names/', include('rest.urls')),
     url(r'^sprintero/slack/', SlackPOSTView.as_view(), name='slack-post'),
]
