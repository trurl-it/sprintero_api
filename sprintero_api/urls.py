# -*- coding: utf-8 -*-
"""sprintero_api URL Configuration"""

from django.conf.urls import url, include

from core.views import index_view
from rest.views import SlackPOSTView, SlackOauthView

urlpatterns = [
     url(r'^$', index_view),
     url(r'^sprintero/names/', include('rest.urls')),
     url(r'^sprintero/slack/$', SlackPOSTView.as_view(), name='slack-post'),
     url(r'^sprintero/auth/$', SlackOauthView.as_view(), name='slack-auth')
]
