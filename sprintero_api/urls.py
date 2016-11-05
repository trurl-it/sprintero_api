# -*- coding: utf-8 -*-
"""sprintero_api URL Configuration"""

from django.conf.urls import url, include

urlpatterns = [
     url(r'^sprintero/names/', include('rest.urls')),
]
