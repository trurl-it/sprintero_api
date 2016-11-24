# -*- coding: utf-8 -*-
"""sprintero_api URL Configuration"""

from django.conf.urls import url, include

from core.views import index_view, success_view
from rest.views import SlackPOSTView, SlackOauthView

urlpatterns = [
     url(r'^$', index_view),
     url(r'^success/(?P<team_domain>[A-Za-z0-9-_.]+)/$', success_view, name='index-view'),
     url(r'^sprintero/names/', include('rest.urls'), name='success-view'),
     url(r'^sprintero/slack/$', SlackPOSTView.as_view(), name='slack-post'),
     url(r'^sprintero/auth/$', SlackOauthView.as_view(), name='slack-auth')
]
